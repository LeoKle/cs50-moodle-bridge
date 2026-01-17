from abc import ABC, abstractmethod

from models.course import CourseCreate, CourseOut


class CourseServiceInterface(ABC):
    @abstractmethod
    def get_courses(self) -> list[CourseOut]: ...

    @abstractmethod
    def get_course(self, course_id: str) -> CourseOut: ...

    @abstractmethod
    def create_course(
        self, course: CourseCreate | str, cs50_id: int | None = None
    ) -> CourseOut: ...
