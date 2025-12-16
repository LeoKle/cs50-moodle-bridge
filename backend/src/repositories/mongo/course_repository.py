from pymongo.collection import Collection

from interfaces.repositories.course_repository_interface import ICourseRepository
from models.course import Course


class MongoCourseRepository(ICourseRepository):
    def __init__(self, collection: Collection):
        self._collection = collection

    def create(self, data: Course) -> Course:
        document = data.model_dump()
        self._collection.insert_one(document)
        return data

    def get(self, item_id: str) -> Course | None:
        doc = self._collection.find_one({"id": item_id})
        return Course(**doc) if doc else None

    def get_all(self) -> list[Course]:
        return [Course(**doc) for doc in self._collection.find()]

    def update(self, item_id: str, data: Course) -> Course | None:
        document = data.model_dump()

        result = self._collection.find_one_and_replace(
            {"id": item_id},
            document,
            return_document=True,
        )

        return Course(**result) if result else None

    def delete(self, item_id: str) -> bool:
        result = self._collection.delete_one({"id": item_id})
        return result.deleted_count == 1
