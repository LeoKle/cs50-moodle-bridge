"""MongoDB implementation of CourseRepository."""

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.database import Database
from repositories import CourseRepository

from models.models import Course


class MongoDBCourseRepository(CourseRepository):
    """MongoDB adapter implementing CourseRepository interface."""

    def __init__(self, db: Database) -> None:
        self.db = db
        self.collection = db.courses
        self._initialize_indexes()

    # def _initialize_indexes(self) -> None:
    #    self.collection.create_index([("cs50_id", 1)], unique=True)
    #    self.collection.create_index([("name", 1)])

    def create(self, course: Course) -> Course:
        doc = course.model_dump(by_alias=True, exclude={"id"})
        result = self.collection.insert_one(doc)
        course.id = str(result.inserted_id)
        return course

    def get(self, course_id: str) -> Course | None:
        try:
            doc = self.collection.find_one({"_id": ObjectId(course_id)})
        except (InvalidId, TypeError, ValueError):
            return None
        else:
            if doc:
                doc["_id"] = str(doc["_id"])
                return Course(**doc)
            return None

    def get_all(self) -> list[Course]:
        courses = []
        for doc in self.collection.find():
            doc["_id"] = str(doc["_id"])
            courses.append(Course(**doc))
        return courses

    def update(self, course_id: str, course: Course) -> Course | None:
        try:
            doc = course.model_dump(by_alias=True, exclude={"id"})
            result = self.collection.find_one_and_update(
                {"_id": ObjectId(course_id)},
                {"$set": doc},
                return_document=True,
            )
        except (InvalidId, TypeError, ValueError):
            return None
        else:
            if result:
                result["_id"] = str(result["_id"])
                return Course(**result)
            return None

    def delete(self, course_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(course_id)})
        except (InvalidId, TypeError, ValueError):
            return False
        else:
            return result.deleted_count > 0
