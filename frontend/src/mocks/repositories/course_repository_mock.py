"""Mock course repository for testing/development."""

from interfaces.repositories.course_repository_interface import (
    CourseRepositoryInterface,
)
from models.course import CourseCreate, CourseOut, CourseUpdate


class MockCourseRepository(CourseRepositoryInterface):
    """In-memory mock implementation for development and testing."""

    def __init__(self):
        """Initialize repository with sample data."""
        self._courses: dict[str, CourseOut] = {
            "507f1f77bcf86cd799439011": CourseOut(
                id="507f1f77bcf86cd799439011",
                name="Introduction to Computer Science",
                cs50_id=101,
                exercise_ids=["ex001", "ex002", "ex003"],
            ),
            "507f1f77bcf86cd799439012": CourseOut(
                id="507f1f77bcf86cd799439012",
                name="Web Programming",
                cs50_id=102,
                exercise_ids=["ex101", "ex102"],
            ),
            "507f1f77bcf86cd799439013": CourseOut(
                id="507f1f77bcf86cd799439013",
                name="Data Structures and Algorithms",
                cs50_id=103,
                exercise_ids=[],
            ),
        }
        self._next_id = 14

    def get_all(self) -> list[CourseOut]:
        """Return all mock courses."""
        return list(self._courses.values())

    def get_by_id(self, course_id: str) -> CourseOut:
        """Return a single course by ID."""
        if course_id not in self._courses:
            msg = f"Course with ID {course_id} not found"
            raise ValueError(msg)
        return self._courses[course_id]

    def create(self, course: CourseCreate) -> CourseOut:
        """Create a new mock course."""
        # Generate a new mock ID
        new_id = f"507f1f77bcf86cd7994390{self._next_id:02d}"
        self._next_id += 1

        new_course = CourseOut(
            id=new_id,
            name=course.name,
            cs50_id=course.cs50_id,
            exercise_ids=course.exercise_ids or [],
        )
        self._courses[new_id] = new_course
        return new_course

    def update(self, course_id: str, course: CourseUpdate) -> CourseOut:
        """Update an existing mock course."""
        if course_id not in self._courses:
            msg = f"Course with ID {course_id} not found"
            raise ValueError(msg)

        existing = self._courses[course_id]
        updated_data = existing.model_dump()

        # Update only provided fields
        if course.name is not None:
            updated_data["name"] = course.name
        if course.cs50_id is not None:
            updated_data["cs50_id"] = course.cs50_id
        if course.exercise_ids is not None:
            updated_data["exercise_ids"] = course.exercise_ids

        updated_course = CourseOut(**updated_data)
        self._courses[course_id] = updated_course
        return updated_course

    def delete(self, course_id: str) -> bool:
        """Delete a course by ID."""
        if course_id not in self._courses:
            return False
        del self._courses[course_id]
        return True
