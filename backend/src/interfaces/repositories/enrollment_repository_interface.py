from abc import ABC, abstractmethod

from models.enrollment import EnrollmentModel


class IEnrollmentRepository(ABC):
    @abstractmethod
    def add_enrollment(self, enrollment: EnrollmentModel): ...

    @abstractmethod
    def get_courses_for_student(self, student_id: str) -> list[str]: ...

    @abstractmethod
    def get_students_for_course(self, course_id: str) -> list[str]: ...

    @abstractmethod
    def remove_enrollment(self, enrollment: EnrollmentModel) -> bool: ...

    @abstractmethod
    def add_bulk_enrollments(self, enrollments: list[EnrollmentModel]): ...
