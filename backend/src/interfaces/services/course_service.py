from abc import ABC, abstractmethod

from models.course import Course


class ICourseService(ABC):
    @abstractmethod
    def get_course(self, course_id: str) -> Course | None: ...

    @abstractmethod
    def get_courses(self, course_id: str) -> list[Course]: ...

    @abstractmethod
    def create_course(self, course: Course): ...

    @abstractmethod
    def update_course(self, course_id: str, course: Course) -> Course: ...

    @abstractmethod
    def delete_course(self, course_id: str): ...
