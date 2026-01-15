"""Interface definition for enrollment service implementations."""

from abc import ABC, abstractmethod


class EnrollmentServiceInterface(ABC):
    """Interface for enrollment-related operations."""

    @abstractmethod
    def upload_enrollment_csv(self, course_id: str, file) -> dict:
        """
        Upload a CSV file containing student enrollment data.

        Args:
            course_id: The ID of the course to enroll students in
            file: The CSV file containing student data

        Returns:
            dict: Result of the enrollment operation

        Raises:
            EnrollmentServiceError: If the upload fails
        """
        ...
