"""Enrollment service - business logic for enrollment operations."""

from typing import Any

from interfaces.repositories.enrollment_repository_interface import (
    EnrollmentRepositoryInterface,
)
from interfaces.services.enrollment_service_interface import EnrollmentServiceInterface


class EnrollmentServiceError(Exception):
    """Custom exception for EnrollmentService errors."""


class EnrollmentService(EnrollmentServiceInterface):
    """Production enrollment service using repository pattern."""

    def __init__(self, repository: EnrollmentRepositoryInterface) -> None:
        """
        Initialize the EnrollmentService with repository injection.

        Args:
            repository: The repository implementation for data access
        """
        self._repository = repository

    def upload_enrollment_csv(self, course_id: str, file: Any) -> dict:
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
            if not course_id or not course_id.strip():
                raise ValueError("Course ID cannot be empty")

            if not file:
                raise ValueError("File is required")

            return self._repository.upload_csv(course_id, file)

        except Exception as e:
            msg = f"Failed to upload enrollment CSV: {e!s}"
            raise EnrollmentServiceError(msg) from e
