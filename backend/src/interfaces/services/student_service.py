from abc import ABC, abstractmethod

from models.student import StudentModel


class IStudentService(ABC):
    @abstractmethod
    def get_student(self, student_id: str) -> StudentModel | None: ...

    @abstractmethod
    def get_students(self, student_id: str) -> list[StudentModel]: ...

    @abstractmethod
    def create_student(self, student: StudentModel): ...

    @abstractmethod
    def update_student(self, student_id: str, student: StudentModel) -> StudentModel: ...

    @abstractmethod
    def delete_student(self, student_id: str): ...

    @abstractmethod
    def get_student_by_email(self, student_email: str) -> StudentModel | None: ...
