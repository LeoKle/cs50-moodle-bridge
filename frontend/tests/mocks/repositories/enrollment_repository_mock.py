"""Mock implementation of EnrollmentRepository for testing."""

from typing import Any

from interfaces.repositories.enrollment_repository_interface import (
    EnrollmentRepositoryInterface,
)


class MockEnrollmentRepositoryError(Exception):
    """Custom exception for MockEnrollmentRepository errors."""


class MockEnrollmentRepository(EnrollmentRepositoryInterface):
    """Mock implementation of EnrollmentRepository for unit testing."""

    def __init__(self):
        """Initialize the mock repository."""
        self._upload_history: list[dict] = []

    def upload_csv(self, course_id: str, file: Any) -> dict:
        """Mock CSV upload - doesn't actually parse, just validates inputs."""
        if not course_id:
            msg = "Course ID is required"
            raise MockEnrollmentRepositoryError(msg)

        if not file:
            msg = "File is required"
            raise MockEnrollmentRepositoryError(msg)

        # Record the upload attempt
        upload_record = {
            "course_id": course_id,
            "filename": getattr(file, "name", "unknown"),
        }
        self._upload_history.append(upload_record)

        # Return mock success response
        return {
            "status": "success",
            "course_id": course_id,
            "enrolled_count": 1,
            "total_students": 1,
        }

    def reset(self) -> None:
        """Reset the mock repository data."""
        self._upload_history.clear()

    def get_upload_history(self) -> list[dict]:
        """Get the history of uploads for testing."""
        return self._upload_history.copy()
