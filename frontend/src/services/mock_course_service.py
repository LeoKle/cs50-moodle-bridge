"""Mock course service for standalone frontend testing."""

from interfaces.services import CourseServiceInterface
from models.course import CourseCreate, CourseOut


class MockCourseService(CourseServiceInterface):
    """Mock implementation of CourseService for testing without backend."""

    def __init__(self) -> None:
        """Initialize the mock service with sample data."""
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

    def get_courses(self) -> list[CourseOut]:
        """Return all mock courses."""
        return list(self._courses.values())

    def get_course(self, course_id: str) -> CourseOut:
        """Return a single course by ID."""
        if course_id not in self._courses:
            msg = f"Course with ID {course_id} not found"
            raise ValueError(msg)
        return self._courses[course_id]

    def create_course(self, course: CourseCreate | str, cs50_id: int | None = None) -> CourseOut:
        """Create a new mock course and add it to the collection."""
        if isinstance(course, str):
            payload = CourseCreate(name=course, cs50_id=cs50_id)
        else:
            payload = CourseCreate.model_validate(course)

        # Generate a new mock ID
        new_id = f"507f1f77bcf86cd7994390{self._next_id:02d}"
        self._next_id += 1

        new_course = CourseOut(
            id=new_id,
            name=payload.name,
            cs50_id=payload.cs50_id,
            exercise_ids=payload.exercise_ids or [],
        )
        self._courses[new_id] = new_course
        return new_course

    def delete_course(self, course_id: str) -> None:
        """Delete a course by ID."""
        if course_id not in self._courses:
            msg = f"Course with ID {course_id} not found"
            raise ValueError(msg)
        del self._courses[course_id]
