"""Mock enrollment repository for testing/development."""

from typing import Any

from interfaces.repositories.enrollment_repository_interface import (
    EnrollmentRepositoryInterface,
)


class MockEnrollmentRepository(EnrollmentRepositoryInterface):
    """In-memory mock implementation for development and testing."""

    def __init__(self):
        """Initialize repository."""
        self._upload_history: list[dict] = []

    def upload_csv(self, course_id: str, file: Any) -> dict:
        """
        Simulate CSV upload.

        Args:
            course_id: The ID of the course to enroll students in
            file: The CSV file object

        Returns:
            dict: Mock enrollment result
        """
        # Simulate successful enrollment
        result = {
            "course_id": course_id,
            "filename": getattr(file, "name", "mock_enrollment.csv"),
            "students_enrolled": 5,
            "status": "success",
            "message": "Mock enrollment completed successfully",
        }

        self._upload_history.append(result)
        return result

    def get_upload_history(self) -> list[dict]:
        """Get history of uploads (for testing purposes)."""
        return self._upload_history.copy()
