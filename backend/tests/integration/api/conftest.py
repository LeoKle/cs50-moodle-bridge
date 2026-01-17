import pytest
from fastapi.testclient import TestClient

from api.app import app, container
from api.v1.controllers import course
from services.course import CourseService


@pytest.fixture
def client_course(course_repository):
    """
    Provides a FastAPI TestClient with a clean container for each test.
    Dependencies can be overridden before yielding the client.
    """
    container.reset_override()

    course_service = CourseService(course_repository)

    container.course_service.override(course_service)

    container.wire(modules=[course])

    with TestClient(app) as c:
        yield c
