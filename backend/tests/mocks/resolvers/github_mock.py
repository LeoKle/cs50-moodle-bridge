from typing import Any

import requests


class MockGitHubResponse:
    def __init__(self, *, status_code: int, json_data: dict[str, Any] | None = None) -> None:
        self.status_code = status_code
        self._json_data = json_data or {}
        self.raise_for_status_called = False

    def json(self) -> dict[str, Any]:
        return self._json_data

    def raise_for_status(self) -> None:
        self.raise_for_status_called = True
        if self.status_code >= 400:
            msg = f"HTTP {self.status_code}"
            raise requests.HTTPError(msg)


class MockRequestsSession:
    def __init__(self) -> None:
        self.post_call_count = 0
        self.last_post_url: str | None = None
        self.last_post_headers: dict[str, str] | None = None
        self.next_post_response: MockGitHubResponse = MockGitHubResponse(
            status_code=200, json_data={}
        )

        self.get_call_count = 0
        self.last_get_url: str | None = None
        self.last_get_headers: dict[str, str] | None = None
        self.next_get_response: MockGitHubResponse = MockGitHubResponse(
            status_code=200, json_data={}
        )

    def post(self, url: str, headers: dict[str, str] | None = None) -> MockGitHubResponse:
        self.post_call_count += 1
        self.last_post_url = url
        self.last_post_headers = dict(headers or {})
        return self.next_post_response

    def get(self, url: str, headers: dict[str, str] | None = None) -> MockGitHubResponse:
        self.get_call_count += 1
        self.last_get_url = url
        self.last_get_headers = dict(headers or {})
        return self.next_get_response
