from abc import ABC

from interfaces.repositories.repository_interface import IRepository
from models.student import StudentModel


class IStudentRepository(IRepository[StudentModel], ABC):
    def get_by_email(self, email: str) -> StudentModel: ...
