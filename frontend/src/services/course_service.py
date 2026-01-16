"""Course service - business logic for course operations."""

from interfaces.repositories.course_repository_interface import (
    CourseRepositoryInterface,
)
from interfaces.services import CourseServiceInterface
from models.course import CourseCreate, CourseOut


class CourseServiceError(Exception):
    """Custom exception for CourseService errors."""


class CourseService(CourseServiceInterface):
    """Production course service using repository pattern."""

    def __init__(self, repository: CourseRepositoryInterface) -> None:
        """
        Initialize the CourseService with repository injection.

        Args:
            repository: The repository implementation for data access
        """
        self._repository = repository

    def get_courses(self) -> list[CourseOut]:
        """
        Get all courses with business logic.

        Returns sorted list of courses by name.
        """
        try:
            courses = self._repository.get_all()
            return sorted(courses, key=lambda c: c.name)
        except Exception as e:
            msg = f"Failed to fetch courses: {e!s}"
            raise CourseServiceError(msg) from e

    def get_course(self, course_id: str) -> CourseOut:
        """
        Get a single course by ID.

        Args:
            course_id: The course ID to fetch

        Returns:
            CourseOut: The requested course
        """
        try:
            return self._repository.get_by_id(course_id)
        except Exception as e:
            msg = f"Failed to fetch course: {e!s}"
            raise CourseServiceError(msg) from e

    def create_course(self, course: CourseCreate | str, cs50_id: int | None = None) -> CourseOut:
        """
        Create a new course with validation.

        Args:
            course: CourseCreate object or course name string
            cs50_id: Optional CS50 course ID

        Returns:
            CourseOut: The created course
        """
        # Convert string to CourseCreate if needed
        payload = (
            CourseCreate(name=course, cs50_id=cs50_id)
            if isinstance(course, str)
            else CourseCreate.model_validate(course)
        )

        def _validate_course_name() -> None:
            if not payload.name or not payload.name.strip():
                msg = "Course name cannot be empty"
                raise ValueError(msg)

        _validate_course_name()

        try:
            return self._repository.create(payload)
        except Exception as e:
            msg = f"Failed to create course: {e!s}"
            raise CourseServiceError(msg) from e

    def delete_course(self, course_id: str) -> None:
        """
        Delete a course by ID.

        Args:
            course_id: The course ID to delete
        """
        try:
            self._repository.delete(course_id)
        except Exception as e:
            msg = f"Failed to delete course: {e!s}"
            raise CourseServiceError(msg) from e
