import base64
import time
from typing import Any

import jwt
import requests

from settings import Settings
from src.interfaces.services.github_user_service_interface import IGitHubUserClient


class GitHubClient(IGitHubUserClient):
    GITHUB_API = "https://api.github.com"
    _ACCEPT = "application/vnd.github+json"

    def __init__(
        self,
        app_id: int | None = None,
        installation_id: int | None = None,
        private_key_base64: str | None = None,
        use_auth: bool | None = None,
    ) -> None:
        cfg = Settings().github

        self.app_id = cfg.app_id if app_id is None else app_id
        self.installation_id = cfg.installation_id if installation_id is None else installation_id
        self.private_key_base64 = (
            cfg.private_key_base64 if private_key_base64 is None else private_key_base64
        )
        self.use_auth = cfg.use_auth if use_auth is None else use_auth

        self._token: str | None = None
        self._token_expires_at: float = 0.0

        if self.use_auth:
            self._refresh_token()

    @staticmethod
    def _now() -> float:
        return time.time()

    @classmethod
    def _accept_headers(cls) -> dict[str, str]:
        return {"Accept": cls._ACCEPT}

    def _refresh_token(self) -> None:
        private_key = base64.b64decode(self.private_key_base64).decode("utf-8")
        now = int(self._now())

        payload = {"iat": now - 60, "exp": now + 5 * 60, "iss": self.app_id}
        jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

        url = f"{self.GITHUB_API}/app/installations/{self.installation_id}/access_tokens"
        headers = {
            **self._accept_headers(),
            "Authorization": f"Bearer {jwt_token}",
        }

        resp = requests.post(url, headers=headers)
        resp.raise_for_status()

        data: dict[str, Any] = resp.json()
        self._token = str(data["token"])
        self._token_expires_at = self._now() + 55 * 60  # refresh early

    def _get_headers(self) -> dict[str, str]:
        if not self.use_auth:
            return self._accept_headers()

        if self._token is None or self._now() >= self._token_expires_at:
            self._refresh_token()

        return {
            **self._accept_headers(),
            "Authorization": f"token {self._token}",
        }

    def get_user_id(self, username: str) -> int | None:
        url = f"{self.GITHUB_API}/users/{username}"
        resp = requests.get(url, headers=self._get_headers())

        if resp.status_code == 200:
            user_id = resp.json().get("id")
            return int(user_id) if user_id is not None else None

        if resp.status_code == 404:
            return None

        resp.raise_for_status()
        return None
