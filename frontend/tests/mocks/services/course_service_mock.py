from typing import Any

from interfaces.services import CourseServiceInterface


class CourseServiceMockError(Exception):
    """Custom exception for CourseService mock errors."""


class MockCourseService(CourseServiceInterface):
    """Mock implementation of CourseService for testing."""

    def __init__(self):
        self._data: dict[str, dict[str, Any]] = {}
        self._id_counter = 1

    def get_courses(self) -> list[dict[str, Any]]:
        """Fetch all courses."""
        return list(self._data.values())

    def get_course(self, course_id: str) -> dict[str, Any]:
        """Fetch a single course by ID."""
        if course_id not in self._data:
            msg = f"Course with id {course_id} not found"
            raise CourseServiceMockError(msg)
        return self._data[course_id]

    def create_course(self, name: str, cs50_id: int | None = None) -> dict[str, Any]:
        """Create a new course."""
        course_id = str(self._id_counter)
        self._id_counter += 1

        course = {
            "id": course_id,
            "name": name,
            "cs50_id": cs50_id,
            "exercise_ids": [],
        }
        self._data[course_id] = course
        return course

    def reset(self) -> None:
        """Reset the mock data."""
        self._data.clear()
        self._id_counter = 1
