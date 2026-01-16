"""Enrollment repository - handles HTTP communication with backend API."""

from typing import Any

import httpx

import constants as const
from config.settings import get_api_settings
from interfaces.repositories.enrollment_repository_interface import (
    EnrollmentRepositoryInterface,
)


class EnrollmentRepositoryError(Exception):
    """Custom exception for EnrollmentRepository errors."""


class EnrollmentRepository(EnrollmentRepositoryInterface):
    """Production implementation - calls actual backend API."""

    def __init__(self):
        """Initialize repository with HTTP client."""
        self._settings = get_api_settings()
        self._client = httpx.Client(
            base_url=self._settings.backend_url, timeout=self._settings.timeout
        )
        self._api_path = f"{const.API_V1_PREFIX}{const.ENROLLMENT_ENDPOINT}"

    def upload_csv(self, course_id: str, file: Any) -> dict:
        """
        Upload enrollment CSV file to backend API.

        Args:
            course_id: The ID of the course to enroll students in
            file: The CSV file object (UploadedFile from Streamlit)

        Returns:
            dict: Result of the enrollment operation

        Raises:
            EnrollmentRepositoryError: If the upload fails
        """
        try:
            files = {"file": (file.name, file, "text/csv")}
            response = self._client.post(f"{self._api_path}/{course_id}", files=files)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            msg = f"Failed to upload enrollment CSV: {e!s}"
            raise EnrollmentRepositoryError(msg) from e

    def __del__(self):
        """Cleanup HTTP client on deletion."""
        if hasattr(self, "_client"):
            self._client.close()
