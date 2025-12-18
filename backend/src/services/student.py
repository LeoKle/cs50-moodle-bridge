from interfaces.repositories.student_repository_interface import IStudentRepository
from interfaces.services.student_service import IStudentService
from models.student import StudentModel


class StudentService(IStudentService):
    def __init__(self, student_repository: IStudentRepository):
        self.student_repository = student_repository

    def get_student(self, student_id: str) -> StudentModel | None:
        record = self.student_repository.get(student_id)
        if record is None:
            return None
        return record

    def get_student_by_email(self, student_email: str) -> StudentModel | None:
        record = self.student_repository.get_by_email(student_email)
        if record is None:
            return None
        return record

    def get_students(self) -> list[StudentModel]:
        records = self.student_repository.get_all()
        return records

    def create_student(self, student: StudentModel):
        created = self.student_repository.create(student)
        return created

    def update_student(self, student_id: str, student: StudentModel) -> StudentModel:
        updated = self.student_repository.update(student_id, student)
        return updated

    def delete_student(self, student_id: str):
        return self.student_repository.delete(student_id)
