import mongomock
import pytest

from repositories.mongo.course_repository import MongoCourseRepository
from repositories.mongo.migration import init_student_collection
from repositories.mongo.student_repository import MongoStudentRepository


@pytest.fixture
def course_repository():
    client = mongomock.MongoClient()
    db = client["test_db"]
    collection = db["courses"]
    return MongoCourseRepository(collection=collection)


@pytest.fixture
def student_repository():
    client = mongomock.MongoClient()
    db = client["test_db"]
    collection = db["students"]
    init_student_collection(collection)
    return MongoStudentRepository(collection=collection)
