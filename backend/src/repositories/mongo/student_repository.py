from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from exceptions.duplicate_email import StudentEmailAlreadyExists
from interfaces.repositories.student_repository_interface import IStudentRepository
from models.student import StudentModel


class MongoStudentRepository(IStudentRepository):
    def __init__(self, collection: Collection):
        self._collection = collection

    def create(self, data: StudentModel) -> StudentModel:
        try:
            self._collection.insert_one(data.model_dump())
        except DuplicateKeyError:
            raise StudentEmailAlreadyExists(data.email) from None
        else:
            return data

    def get(self, item_id: str) -> StudentModel | None:
        doc = self._collection.find_one({"id": item_id})
        return StudentModel(**doc) if doc else None

    def get_all(self) -> list[StudentModel]:
        return [StudentModel(**doc) for doc in self._collection.find()]

    def update(self, item_id: str, data: StudentModel) -> StudentModel | None:
        document = data.model_dump()

        result = self._collection.find_one_and_replace(
            {"id": item_id},
            document,
            return_document=True,
        )

        return StudentModel(**result) if result else None

    def delete(self, item_id: str) -> bool:
        result = self._collection.delete_one({"id": item_id})
        return result.deleted_count == 1

    def get_by_email(self, email: str) -> StudentModel | None:
        result = self._collection.find_one({"email": email})

        return StudentModel(**result) if result else None
