import pytest

from resolvers.github.client import GitHubClient
from tests.mocks.resolvers.github_mock import MockGitHubResponse, MockRequestsSession

pytestmark = pytest.mark.unit


class DummyAuthProvider:
    def __init__(self, headers: dict[str, str] | None = None) -> None:
        self._headers = headers or {"Accept": "application/vnd.github+json"}
        self.get_headers_called = False

    def get_headers(self) -> dict[str, str]:
        self.get_headers_called = True
        return dict(self._headers)


@pytest.fixture
def auth_provider() -> DummyAuthProvider:
    return DummyAuthProvider(headers={"Accept": "application/vnd.github+json", "X-Test": "true"})


@pytest.fixture
def requests_session() -> MockRequestsSession:
    return MockRequestsSession()


@pytest.fixture
def github_client(
    auth_provider: DummyAuthProvider,
    requests_session: MockRequestsSession,
) -> GitHubClient:
    return GitHubClient(auth=auth_provider, session=requests_session)


def test_get_user_id_returns_id_when_user_exists(
    github_client: GitHubClient,
    requests_session: MockRequestsSession,
    auth_provider: DummyAuthProvider,
) -> None:
    requests_session.next_get_response = MockGitHubResponse(
        status_code=200,
        json_data={"id": 12345},
    )

    user_id = github_client.get_user_id("octocat")

    assert user_id == 12345
    assert auth_provider.get_headers_called is True
    assert requests_session.get_call_count == 1
    assert requests_session.last_get_url == "https://api.github.com/users/octocat"
    assert requests_session.last_get_headers == {
        "Accept": "application/vnd.github+json", "X-Test": "true",
    }


def test_get_user_id_returns_none_when_user_not_found(
    github_client: GitHubClient,
    requests_session: MockRequestsSession,
) -> None:
    requests_session.next_get_response = MockGitHubResponse(
        status_code=404,
        json_data={},
    )

    user_id = github_client.get_user_id("unknown-user")

    assert user_id is None
    assert requests_session.next_get_response.raise_for_status_called is False


def test_get_user_id_raises_for_non_404_http_error(
    github_client: GitHubClient,
    requests_session: MockRequestsSession,
) -> None:
    requests_session.next_get_response = MockGitHubResponse(
        status_code=500,
        json_data={},
    )

    with pytest.raises(RuntimeError, match="HTTP 500"):
        github_client.get_user_id("octocat")

    assert requests_session.next_get_response.raise_for_status_called is True


def test_get_user_id_returns_none_when_id_missing_in_response(
    github_client: GitHubClient,
    requests_session: MockRequestsSession,
) -> None:
    requests_session.next_get_response = MockGitHubResponse(
        status_code=200,
        json_data={},
    )

    user_id = github_client.get_user_id("octocat")

    assert user_id is None
    assert requests_session.next_get_response.raise_for_status_called is True
