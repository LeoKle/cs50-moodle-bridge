from interfaces.services import CourseServiceInterface
from modles.course import CourseCreate, CourseOut


class CourseServiceMockError(Exception):
    """Custom exception for CourseService mock errors."""


class MockCourseService(CourseServiceInterface):
    """Mock implementation of CourseService for testing."""

    def __init__(self):
        self._data: dict[str, CourseOut] = {}
        self._id_counter = 1

    def get_courses(self) -> list[CourseOut]:
        """Fetch all courses."""
        return list(self._data.values())

    def get_course(self, course_id: str) -> CourseOut:
        """Fetch a single course by ID."""
        if course_id not in self._data:
            msg = f"Course with id {course_id} not found"
            raise CourseServiceMockError(msg)
        return self._data[course_id]

    def create_course(self, course: CourseCreate | str, cs50_id: int | None = None) -> CourseOut:
        """Create a new course."""
        course_id = str(self._id_counter)
        self._id_counter += 1

        payload = (
            CourseCreate(name=course, cs50_id=cs50_id)
            if isinstance(course, str)
            else CourseCreate.model_validate(course)
        )

        course_out = CourseOut.model_validate({
            "id": course_id,
            "name": payload.name,
            "cs50_id": payload.cs50_id,
            "exercise_ids": payload.exercise_ids or [],
        })
        self._data[course_id] = course_out
        return course_out

    def reset(self) -> None:
        """Reset the mock data."""
        self._data.clear()
        self._id_counter = 1
