"""Mock enrollment service for standalone frontend testing."""

from interfaces.services.enrollment_service_interface import EnrollmentServiceInterface


class MockEnrollmentService(EnrollmentServiceInterface):
    """Mock implementation of EnrollmentService for testing without backend."""

    def __init__(self) -> None:
        """Initialize the mock enrollment service."""
        self.uploaded_files: list[dict] = []

    def upload_enrollment_csv(self, course_id: str, file) -> dict:
        """
        Simulate CSV file upload and return mock success response.

        Args:
            course_id: The ID of the course to enroll students in
            file: The CSV file object

        Returns:
            dict: Mock result of the enrollment operation
        """
        # Read the file content for validation (optional)
        try:
            content = file.read()
            if isinstance(content, bytes):
                content = content.decode("utf-8")

            # Parse CSV to count students
            lines = content.strip().split("\n")
            # Assuming first line is header
            student_count = max(0, len(lines) - 1)

            # Reset file pointer for potential re-reads
            file.seek(0)

        except (ValueError, KeyError, UnicodeDecodeError):
            student_count = 0

        # Store upload info for testing purposes
        upload_info = {
            "course_id": course_id,
            "filename": getattr(file, "name", "unknown.csv"),
            "student_count": student_count,
        }
        self.uploaded_files.append(upload_info)

        # Return mock success response
        return {
            "status": "success",
            "message": f"Successfully enrolled {student_count} students in course {course_id}",
            "enrolled_count": student_count,
            "failed_count": 0,
            "details": {
                "enrolled_students": [
                    f"student_{i}@example.com" for i in range(1, min(student_count + 1, 6))
                ],
                "failed_students": [],
            },
        }
