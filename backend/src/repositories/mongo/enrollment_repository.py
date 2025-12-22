from pymongo.collection import Collection

from interfaces.repositories.enrollment_repository_interface import IEnrollmentRepository
from models.enrollment import EnrollmentModel


class MongoEnrollmentRepository(IEnrollmentRepository):
    def __init__(self, collection: Collection):
        self._collection = collection

    def add_enrollment(self, enrollment: EnrollmentModel):
        document = enrollment.model_dump()

        self._collection.insert_one(document)

    def get_courses_for_student(self, student_id: str) -> list[str]:
        docs = self._collection.find({"student_id": student_id})
        return [doc["course_id"] for doc in docs]

    def get_students_for_course(self, course_id: str) -> list[str]:
        docs = self._collection.find({"course_id": course_id})
        return [doc["student_id"] for doc in docs]

    def remove_enrollment(self, enrollment: EnrollmentModel) -> bool:
        result = self._collection.delete_one({
            "student_id": enrollment.student_id,
            "course_id": enrollment.course_id,
        })
        return result.deleted_count == 1

    def add_bulk_enrollments(self, enrollments: list[EnrollmentModel]):
        if not enrollments:
            return

        documents = [e.model_dump() for e in enrollments]
        self._collection.insert_many(documents)
