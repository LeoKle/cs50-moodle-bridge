"""Course repository interface."""

from abc import ABC, abstractmethod

from models.course import CourseCreate, CourseOut, CourseUpdate


class CourseRepositoryInterface(ABC):
    """Interface for course data access."""

    @abstractmethod
    def get_all(self) -> list[CourseOut]:
        """Fetch all courses."""
        pass

    @abstractmethod
    def get_by_id(self, course_id: str) -> CourseOut:
        """Fetch course by ID."""
        pass

    @abstractmethod
    def create(self, course: CourseCreate) -> CourseOut:
        """Create new course."""
        pass

    @abstractmethod
    def update(self, course_id: str, course: CourseUpdate) -> CourseOut:
        """Update existing course."""
        pass

    @abstractmethod
    def delete(self, course_id: str) -> bool:
        """Delete course."""
        pass
