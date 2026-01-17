"""Enrollment repository interface."""

from abc import ABC, abstractmethod
from typing import Any


class EnrollmentRepositoryInterface(ABC):
    """Interface for enrollment data access."""

    @abstractmethod
    def upload_csv(self, course_id: str, file: Any) -> dict:
        """
        Upload enrollment CSV file.

        Args:
            course_id: The ID of the course to enroll students in
            file: The CSV file object

        Returns:
            dict: Result of the enrollment operation
        """
        pass
