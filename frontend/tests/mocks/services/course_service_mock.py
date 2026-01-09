from typing import Any, Dict, List


class MockCourseService:
    """Mock implementation of CourseService for testing."""

    def __init__(self):
        self._data: Dict[str, Dict[str, Any]] = {}
        self._id_counter = 1

    def get_courses(self) -> List[Dict[str, Any]]:
        """Fetch all courses."""
        return list(self._data.values())

    def get_course(self, course_id: str) -> Dict[str, Any]:
        """Fetch a single course by ID."""
        if course_id not in self._data:
            raise Exception(f"Course with id {course_id} not found")
        return self._data[course_id]

    def create_course(self, name: str, cs50_id: int | None = None) -> Dict[str, Any]:
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
