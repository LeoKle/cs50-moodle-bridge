from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from api.app import app, container
from api.v1.controllers import course, cs50_submission_problem
from models.course import Course
from tests.mocks.services.course_service_mock import MockCourseService
from tests.mocks.services.cs50_submission_problem_service_mock import (
    MockCS50SubmissionProblemService,
)


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

    container.cs50_submission_problem_service.override(MockCS50SubmissionProblemService())
    container.wire(modules=[course, cs50_submission_problem])

    with TestClient(app) as c:
        yield c


@pytest.fixture
def cs50_submission_problem_fixture():
    mock_cs50_service = container.cs50_submission_problem_service()

    mock_cs50_service.seed(
        "hsddigitallabor/problems/adg2025/intervals",
        submissions=[
            {
                "archive": "https://github.com/me50/test/archive/abc123.zip",
                "checks_passed": 13,
                "checks_run": 13,
                "github_id": 123,
                "github_url": "https://github.com/me50/test/tree/abc123",
                "github_username": "testuser",
                "name": "Interval Assignment",
                "slug": "hsddigitallabor/problems/adg2025/intervals",
                "timestamp": datetime(2025, 12, 1, 20, 53, 16, tzinfo=UTC).isoformat(),
            }
        ],
    )

    return mock_cs50_service
