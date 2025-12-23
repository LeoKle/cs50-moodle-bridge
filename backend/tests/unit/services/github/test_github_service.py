import time
from collections.abc import Callable
from typing import Any

import pytest

import services.github_client as gh_mod
from services.github_client import GitHubClient

pytestmark = pytest.mark.unit

ACCEPT = "application/vnd.github+json"


class DummyResponse:
    def __init__(self, status_code: int, json_data: dict[str, Any] | None = None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.raise_for_status_called = False

    def json(self) -> dict[str, Any]:
        return self._json_data

    def raise_for_status(self) -> None:
        self.raise_for_status_called = True
        if self.status_code >= 400:
            msg = f"HTTP {self.status_code}"
            raise RuntimeError(msg)


def make_client(*, use_auth: bool) -> GitHubClient:
    return GitHubClient(use_auth=use_auth)


def set_token(client: GitHubClient, token: str | None, *, expires_in_seconds: float) -> None:
    client._token = token
    client._token_expires_at = time.time() + expires_in_seconds


def expect_base_headers(headers: dict[str, str]) -> None:
    assert headers["Accept"] == ACCEPT


def mock_get(monkeypatch, handler: Callable[..., DummyResponse]) -> None:
    monkeypatch.setattr(gh_mod.requests, "get", handler)


def mock_post(monkeypatch, handler: Callable[..., DummyResponse]) -> None:
    monkeypatch.setattr(gh_mod.requests, "post", handler)


@pytest.fixture
def no_auth_client() -> GitHubClient:
    return make_client(use_auth=False)


@pytest.fixture
def auth_client(monkeypatch) -> GitHubClient:
    original_refresh = GitHubClient._refresh_token
    monkeypatch.setattr(GitHubClient, "_refresh_token", lambda self: None)
    client = make_client(use_auth=True)
    monkeypatch.setattr(GitHubClient, "_refresh_token", original_refresh)

    set_token(client, None, expires_in_seconds=-1)
    return client


def test_init_does_not_refresh_when_use_auth_false(monkeypatch):
    def fail_if_called(*_a, **_k):
        msg = "_refresh_token should NOT be called"
        raise AssertionError(msg)

    monkeypatch.setattr(GitHubClient, "_refresh_token", fail_if_called)
    make_client(use_auth=False)


def test_init_refreshes_when_use_auth_true(monkeypatch):
    called = {"n": 0}

    def fake_refresh(self):
        called["n"] += 1
        set_token(self, "INIT_TOKEN", expires_in_seconds=3600)

    monkeypatch.setattr(GitHubClient, "_refresh_token", fake_refresh)
    client = make_client(use_auth=True)

    assert called["n"] == 1
    assert client._token == "INIT_TOKEN"


def test_get_headers_without_auth(no_auth_client):
    assert no_auth_client._get_headers() == {"Accept": ACCEPT}


def test_get_headers_auth_refreshes_when_token_missing(auth_client, monkeypatch):
    def fake_refresh():
        set_token(auth_client, "NEW_TOKEN", expires_in_seconds=3600)

    monkeypatch.setattr(auth_client, "_refresh_token", fake_refresh)

    headers = auth_client._get_headers()
    expect_base_headers(headers)
    assert headers["Authorization"] == "token NEW_TOKEN"


def test_get_headers_auth_refreshes_when_token_expired(auth_client, monkeypatch):
    set_token(auth_client, "OLD_TOKEN", expires_in_seconds=-1)

    def fake_refresh():
        set_token(auth_client, "NEW_TOKEN", expires_in_seconds=3600)

    monkeypatch.setattr(auth_client, "_refresh_token", fake_refresh)

    headers = auth_client._get_headers()
    assert headers["Authorization"] == "token NEW_TOKEN"


def test_get_headers_auth_does_not_refresh_when_token_valid(auth_client, monkeypatch):
    set_token(auth_client, "VALID_TOKEN", expires_in_seconds=3600)

    def fail_if_called():
        msg = "_refresh_token should NOT be called"
        raise AssertionError(msg)

    monkeypatch.setattr(auth_client, "_refresh_token", fail_if_called)

    headers = auth_client._get_headers()
    assert headers["Authorization"] == "token VALID_TOKEN"


def test_refresh_token_sets_token_and_expiration(auth_client, monkeypatch):
    monkeypatch.setattr(gh_mod.jwt, "encode", lambda *_a, **_k: "FAKE_JWT")

    def fake_post(url, headers=None):
        assert url.endswith(f"/app/installations/{auth_client.installation_id}/access_tokens")
        expect_base_headers(headers)
        assert headers["Authorization"] == "Bearer FAKE_JWT"
        return DummyResponse(201, {"token": "INSTALL_TOKEN"})

    mock_post(monkeypatch, fake_post)

    auth_client._refresh_token()

    assert auth_client._token == "INSTALL_TOKEN"
    assert auth_client._token_expires_at > time.time()


def test_get_user_id_returns_id_when_found(no_auth_client, monkeypatch):
    def fake_get(url, headers=None):
        assert url.endswith("/users/octocat")
        assert headers == {"Accept": ACCEPT}
        return DummyResponse(200, {"id": 123})

    mock_get(monkeypatch, fake_get)

    assert no_auth_client.get_user_id("octocat") == 123


def test_get_user_id_returns_none_when_not_found(no_auth_client, monkeypatch):
    mock_get(monkeypatch, lambda *_a, **_k: DummyResponse(404))
    assert no_auth_client.get_user_id("missing-user") is None


def test_get_user_id_raises_on_http_error(no_auth_client, monkeypatch):
    mock_get(monkeypatch, lambda *_a, **_k: DummyResponse(500))
    with pytest.raises(RuntimeError, match="HTTP 500"):
        no_auth_client.get_user_id("octocat")


def test_get_user_id_other_status_returns_none(no_auth_client, monkeypatch):
    resp = DummyResponse(302)
    mock_get(monkeypatch, lambda *_a, **_k: resp)

    assert no_auth_client.get_user_id("octocat") is None
    assert resp.raise_for_status_called is True


def test_get_user_id_with_auth_uses_token_header(auth_client, monkeypatch):
    set_token(auth_client, "OLD_TOKEN", expires_in_seconds=-1)

    def fake_refresh():
        set_token(auth_client, "NEW_TOKEN", expires_in_seconds=3600)

    monkeypatch.setattr(auth_client, "_refresh_token", fake_refresh)

    def fake_get(url, headers=None):
        expect_base_headers(headers)
        assert headers["Authorization"] == "token NEW_TOKEN"
        return DummyResponse(200, {"id": 42})

    mock_get(monkeypatch, fake_get)

    assert auth_client.get_user_id("octocat") == 42
