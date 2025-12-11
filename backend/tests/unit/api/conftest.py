import pytest
from fastapi.testclient import TestClient

from api.app import app, container
from api.v1.controllers import course
from tests.mocks.services.course_service_mock import MockCourseService


@pytest.fixture
def client():
    """
    Provides a FastAPI TestClient with a clean container for each test.
    Dependencies can be overridden before yielding the client.
    """
    container.reset_override()
    container.course_service.override(MockCourseService())

    container.wire(modules=[course])

    with TestClient(app) as c:
        yield c
