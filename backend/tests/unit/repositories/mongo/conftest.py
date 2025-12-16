import mongomock
import pytest

from repositories.mongo.course_repository import MongoCourseRepository


@pytest.fixture
def course_repository():
    client = mongomock.MongoClient()
    db = client["test_db"]
    collection = db["courses"]
    return MongoCourseRepository(collection=collection)
