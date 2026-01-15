"""Enrollment service for handling API calls to the backend."""

import os

import requests

import constants as const
from interfaces.services.enrollment_service_interface import EnrollmentServiceInterface


class EnrollmentServiceError(Exception):
    """Custom exception for EnrollmentService errors."""


class EnrollmentService(EnrollmentServiceInterface):
    """Service to handle enrollment-related API calls to the backend."""

    def __init__(self) -> None:
        """Initialize the EnrollmentService with backend URL configuration."""
        self.base_url = os.getenv("BACKEND_URL", const.DEFAULT_BACKEND_URL)
        self.api_url = f"{self.base_url}{const.API_V1_PREFIX}{const.ENROLLMENT_ENDPOINT}"

    def upload_enrollment_csv(self, course_id: str, file) -> dict:
        """
        Upload a CSV file containing student enrollment data.

        Args:
            course_id: The ID of the course to enroll students in
            file: The CSV file object (UploadedFile from Streamlit)

        Returns:
            dict: Result of the enrollment operation containing success/error information

        Raises:
            EnrollmentServiceError: If the upload fails
        """
        try:
            files = {"file": (file.name, file, "text/csv")}

            response = requests.post(
                f"{self.api_url}/{course_id}",
                files=files,
                timeout=const.REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            msg = f"Failed to upload enrollment CSV: {e!s}"
            raise EnrollmentServiceError(msg) from e
