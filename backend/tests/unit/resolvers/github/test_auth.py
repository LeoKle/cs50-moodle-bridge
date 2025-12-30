import base64

import pytest

import resolvers.github.auth as auth_module
from resolvers.github.auth import AnonymousGitHubAuth, GitHubAppAuth, GitHubAuthProvider
from tests.mocks.resolvers.github_mock import MockGitHubResponse, MockRequestsSession

pytestmark = pytest.mark.unit


@pytest.fixture
def github_accept_header_value() -> str:
    return GitHubAuthProvider.ACCEPT


@pytest.fixture
def github_app_private_key_b64() -> str:
    return base64.b64encode(
        b"-----BEGIN PRIVATE KEY-----\nFAKE\n-----END PRIVATE KEY-----\n"
    ).decode(
        "utf-8"
    )


@pytest.fixture
def fixed_now_seconds() -> float:
    return 1_700_000_000.0


@pytest.fixture
def mock_requests_session() -> MockRequestsSession:
    return MockRequestsSession()


@pytest.fixture
def github_app_auth(
    github_app_private_key_b64: str,
    mock_requests_session: MockRequestsSession,
) -> GitHubAppAuth:
    return GitHubAppAuth(
        app_id=111,
        installation_id=222,
        private_key_b64=github_app_private_key_b64,
        session=mock_requests_session,
        refresh_margin_seconds=60,
    )


def test_accept_headers_returns_expected_accept_header(github_accept_header_value: str) -> None:
    assert GitHubAuthProvider.accept_headers() == {"Accept": github_accept_header_value}


def test_anonymous_auth_returns_only_accept_header(github_accept_header_value: str) -> None:
    anonymous_auth = AnonymousGitHubAuth()
    assert anonymous_auth.get_headers() == {"Accept": github_accept_header_value}


def test_decode_private_key_returns_decoded_string(
    github_app_auth: GitHubAppAuth,
    github_app_private_key_b64: str,
) -> None:
    expected = base64.b64decode(github_app_private_key_b64).decode("utf-8")
    assert github_app_auth.decode_private_key() == expected


def test_refresh_token_makes_expected_post_and_sets_token_and_expiration(
    monkeypatch,
    github_app_auth: GitHubAppAuth,
    mock_requests_session: MockRequestsSession,
    fixed_now_seconds: float,
    github_accept_header_value: str,
) -> None:

    monkeypatch.setattr(GitHubAppAuth, "now", staticmethod(lambda: fixed_now_seconds))
    monkeypatch.setattr(auth_module.jwt, "encode", lambda *_a, **_k: "FAKE_JWT")

    mock_requests_session.next_post_response = MockGitHubResponse(
        status_code=201,
        json_data={"token": "INSTALLATION_TOKEN_123"},
    )

    github_app_auth.refresh_token()

    assert mock_requests_session.post_call_count == 1
    assert mock_requests_session.last_post_url == (
        "https://api.github.com/app/installations/222/access_tokens"
    )

    sent_headers = mock_requests_session.last_post_headers or {}
    assert sent_headers["Accept"] == github_accept_header_value
    assert sent_headers["Authorization"] == "Bearer FAKE_JWT"

    assert github_app_auth._token == "INSTALLATION_TOKEN_123"
    assert github_app_auth._token_expires_at == pytest.approx(fixed_now_seconds + 55 * 60)


def test_ensure_token_refreshes_if_token_is_missing(
    monkeypatch,
    github_app_auth: GitHubAppAuth,
) -> None:
    refresh_calls = {"count": 0}

    def fake_refresh_token() -> None:
        refresh_calls["count"] += 1
        github_app_auth._token = "NEW_TOKEN"
        github_app_auth._token_expires_at = github_app_auth.now() + 3600

    monkeypatch.setattr(github_app_auth, "refresh_token", fake_refresh_token)

    github_app_auth._token = None

    token = github_app_auth.ensure_token()

    assert refresh_calls["count"] == 1
    assert token == "NEW_TOKEN"


def test_ensure_token_refreshes_if_token_is_close_to_expiring(
    monkeypatch,
    github_app_auth: GitHubAppAuth,
    fixed_now_seconds: float,
) -> None:
    monkeypatch.setattr(GitHubAppAuth, "now", staticmethod(lambda: fixed_now_seconds))

    github_app_auth._token = "OLD_TOKEN"
    github_app_auth._token_expires_at = fixed_now_seconds + 50

    refresh_calls = {"count": 0}

    def fake_refresh_token() -> None:
        refresh_calls["count"] += 1
        github_app_auth._token = "REFRESHED_TOKEN"
        github_app_auth._token_expires_at = fixed_now_seconds + 3600

    monkeypatch.setattr(github_app_auth, "refresh_token", fake_refresh_token)

    token = github_app_auth.ensure_token()

    assert refresh_calls["count"] == 1
    assert token == "REFRESHED_TOKEN"


def test_ensure_token_does_not_refresh_if_token_is_valid(
    monkeypatch,
    github_app_auth: GitHubAppAuth,
    fixed_now_seconds: float,
) -> None:
    monkeypatch.setattr(GitHubAppAuth, "now", staticmethod(lambda: fixed_now_seconds))

    github_app_auth._token = "VALID_TOKEN"
    github_app_auth._token_expires_at = fixed_now_seconds + 10_000

    def refresh_should_not_be_called() -> None:
        msg = "refresh_token should NOT be called"
        raise AssertionError(msg)

    monkeypatch.setattr(github_app_auth, "refresh_token", refresh_should_not_be_called)

    assert github_app_auth.ensure_token() == "VALID_TOKEN"


def test_get_headers_returns_accept_and_token_authorization_header(
    monkeypatch,
    github_app_auth: GitHubAppAuth,
    github_accept_header_value: str,
) -> None:
    monkeypatch.setattr(github_app_auth, "ensure_token", lambda: "TOKEN_FOR_HEADERS")

    headers = github_app_auth.get_headers()

    assert headers["Accept"] == github_accept_header_value
    assert headers["Authorization"] == "token TOKEN_FOR_HEADERS"


# test coverage line 20 for abstract method
def test_base_get_headers_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        GitHubAuthProvider.get_headers(None)
