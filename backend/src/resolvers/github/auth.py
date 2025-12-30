import base64
import time
from abc import ABC, abstractmethod
from typing import Any

import jwt
import requests


class GitHubAuthProvider(ABC):
    ACCEPT = "application/vnd.github+json"

    @classmethod
    def accept_headers(cls) -> dict[str, str]:
        return {"Accept": cls.ACCEPT}

    @abstractmethod
    def get_headers(self) -> dict[str, str]:
        raise NotImplementedError


class AnonymousGitHubAuth(GitHubAuthProvider):
    def get_headers(self) -> dict[str, str]:
        return self.accept_headers()


class GitHubAppAuth(GitHubAuthProvider):
    GITHUB_API = "https://api.github.com"

    def __init__(
        self,
        app_id: int,
        installation_id: int,
        private_key_b64: str,
        session: requests.Session | None = None,
        *,
        refresh_margin_seconds: int = 60,
    ) -> None:
        self._app_id = app_id
        self._installation_id = installation_id
        self._private_key_b64 = private_key_b64
        self._session = session or requests.Session()

        self._token: str | None = None
        self._token_expires_at: float = 0.0
        self._refresh_margin_seconds = refresh_margin_seconds

    @staticmethod
    def now() -> float:
        return time.time()

    def decode_private_key(self) -> str:
        return base64.b64decode(self._private_key_b64).decode("utf-8")

    def refresh_token(self) -> None:
        private_key = self.decode_private_key()
        now = int(self.now())

        payload = {"iat": now - 60, "exp": now + 5 * 60, "iss": self._app_id}
        jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

        url = f"{self.GITHUB_API}/app/installations/{self._installation_id}/access_tokens"
        headers = {
            **self.accept_headers(),
            "Authorization": f"Bearer {jwt_token}",
        }

        resp = self._session.post(url, headers=headers)
        resp.raise_for_status()

        data: dict[str, Any] = resp.json()
        self._token = str(data["token"])

        self._token_expires_at = self.now() + 55 * 60

    def ensure_token(self) -> str:
        if self._token is None:
            self.refresh_token()
            return self._token

        if self.now() >= (self._token_expires_at - self._refresh_margin_seconds):
            self.refresh_token()

        return self._token

    def get_headers(self) -> dict[str, str]:
        token = self.ensure_token()
        return {
            **self.accept_headers(),
            "Authorization": f"token {token}",
        }
