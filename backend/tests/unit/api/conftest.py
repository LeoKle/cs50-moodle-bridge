import pytest
from fastapi.testclient import TestClient

from api.app import app, container
from api.v1.controllers import course
from models.course import Course
from tests.mocks.services.course_service_mock import MockCourseService


@pytest.fixture
def client():
    """
    Provides a FastAPI TestClient with a clean container for each test.
    Dependencies can be overridden before yielding the client.
    """
    container.reset_override()

    mock_service = MockCourseService()
    mock_service.create_course(Course(id="1", name="Course 1", cs50_id=50, exercise_ids=[]))
    mock_service.create_course(Course(id="2", name="Course 2", cs50_id=51, exercise_ids=[]))

    container.course_service.override(mock_service)

    container.wire(modules=[course])

    with TestClient(app) as c:
        yield c
