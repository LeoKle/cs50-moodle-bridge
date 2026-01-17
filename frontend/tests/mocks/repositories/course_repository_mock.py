"""Mock implementation of CourseRepository for testing."""

from interfaces.repositories.course_repository_interface import (
    CourseRepositoryInterface,
)
from models.course import CourseCreate, CourseOut, CourseUpdate


class MockCourseRepositoryError(Exception):
    """Custom exception for MockCourseRepository errors."""


class MockCourseRepository(CourseRepositoryInterface):
    """Mock implementation of CourseRepository for unit testing."""

    def __init__(self):
        """Initialize the mock repository."""
        self._data: dict[str, CourseOut] = {}
        self._id_counter = 1

    def get_all(self) -> list[CourseOut]:
        """Fetch all courses from mock storage."""
        return list(self._data.values())

    def get_by_id(self, course_id: str) -> CourseOut:
        """Fetch course by ID from mock storage."""
        if course_id not in self._data:
            msg = f"Course {course_id} not found"
            raise MockCourseRepositoryError(msg)
        return self._data[course_id]

    def create(self, course: CourseCreate) -> CourseOut:
        """Create new course in mock storage."""
        course_id = str(self._id_counter)
        self._id_counter += 1

        course_out = CourseOut.model_validate({
            "id": course_id,
            "name": course.name,
            "cs50_id": course.cs50_id,
            "exercise_ids": course.exercise_ids or [],
        })
        self._data[course_id] = course_out
        return course_out

    def update(self, course_id: str, course: CourseUpdate) -> CourseOut:
        """Update existing course in mock storage."""
        if course_id not in self._data:
            msg = f"Course {course_id} not found"
            raise MockCourseRepositoryError(msg)

        existing = self._data[course_id]
        update_data = course.model_dump(exclude_none=True)

        updated = CourseOut.model_validate({
            "id": existing.id,
            "name": update_data.get("name", existing.name),
            "cs50_id": update_data.get("cs50_id", existing.cs50_id),
            "exercise_ids": update_data.get("exercise_ids", existing.exercise_ids),
        })
        self._data[course_id] = updated
        return updated

    def delete(self, course_id: str) -> bool:
        """Delete course from mock storage."""
        if course_id not in self._data:
            msg = f"Course {course_id} not found"
            raise MockCourseRepositoryError(msg)
        del self._data[course_id]
        return True

    def reset(self) -> None:
        """Reset the mock repository data."""
        self._data.clear()
        self._id_counter = 1

    def seed_data(self, courses: list[CourseOut]) -> None:
        """Seed the repository with initial data for testing."""
        for course in courses:
            self._data[course.id] = course
