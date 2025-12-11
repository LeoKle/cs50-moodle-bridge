"""Repository interfaces for data access (port in clean architecture)."""

from abc import ABC, abstractmethod

from models.course import Course


class CourseRepository(ABC):
    """Repository interface for managing courses."""

    @abstractmethod
    def create(self, course: Course) -> Course:
        pass

    @abstractmethod
    def get(self, course_id: str) -> Course | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Course]:
        pass

    @abstractmethod
    def update(self, course_id: str, course: Course) -> Course | None:
        """Update an existing course.

        Args:
            course_id: MongoDB ObjectId as string
            course: Updated course data
        """
        pass

    @abstractmethod
    def delete(self, course_id: str) -> bool:
        """Delete a course by ID.
        Returns:
            True if deleted, False if not found
        """
        pass
