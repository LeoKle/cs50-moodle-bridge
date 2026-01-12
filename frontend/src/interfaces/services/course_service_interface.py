from abc import ABC, abstractmethod
from typing import Any


class CourseServiceInterface(ABC):

    @abstractmethod
    def get_courses(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    def get_course(self, course_id: str) -> dict[str, Any]: ...

    @abstractmethod
    def create_course(self, name: str, cs50_id: int | None = None) -> dict[str, Any]: ...
