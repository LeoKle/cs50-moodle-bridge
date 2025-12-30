import requests

from interfaces.resolver.github_client_resolver import IGitHubClientResolver
from resolvers.github.auth import GitHubAuthProvider


class GitHubClient(IGitHubClientResolver):
    GITHUB_API = "https://api.github.com"

    def __init__(self, auth: GitHubAuthProvider, session: requests.Session | None = None) -> None:
        self._auth = auth
        self._session = session or requests.Session()

    def get_user_id(self, username: str) -> int | None:
        url = f"{self.GITHUB_API}/users/{username}"
        resp = self._session.get(url, headers=self._auth.get_headers())

        if resp.status_code == 404:
            return None

        try:
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(str(e)) from e

        user_id = resp.json().get("id")
        return int(user_id) if user_id is not None else None
