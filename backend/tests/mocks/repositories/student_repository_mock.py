from exceptions.duplicate_email import StudentEmailAlreadyExists
from interfaces.repositories.course_repository_interface import ICourseRepository
from models.student import StudentModel


class MockStudentRepository(ICourseRepository):
    def __init__(self):
        self._data: dict[str, StudentModel] = {}

    def create(self, data: StudentModel) -> StudentModel:
        if any(s.email == data.email for s in self._data.values()):
            raise StudentEmailAlreadyExists(data.email)
        self._data[data.id] = data
        return data

    def get(self, item_id: str) -> StudentModel | None:
        return self._data.get(item_id)

    def get_all(self) -> list[StudentModel]:
        return list(self._data.values())

    def update(self, item_id: str, data: StudentModel) -> StudentModel | None:
        if item_id not in self._data:
            return None

        self._data[item_id] = data
        return self._data[item_id]

    def delete(self, item_id: str) -> bool:
        if item_id in self._data:
            self._data.pop(item_id)
            return True
        return False

    def get_by_email(self, email: str) -> StudentModel | None:
        for s in self._data.values():
            if s.email == email:
                return s
        return None
