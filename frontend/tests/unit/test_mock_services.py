"""Test mock services to ensure they work correctly."""

import os

import pytest

from models.course import CourseCreate
from services.service_factory import get_course_service, get_enrollment_service


@pytest.fixture(autouse=True)
def set_mock_env(monkeypatch):
    """Set environment to use mock services for all tests in this module."""
    monkeypatch.setenv("USE_MOCK_SERVICES", "true")


def test_mock_course_service_get_courses():
    """Test that mock course service returns sample courses."""
    service = get_course_service()
    courses = service.get_courses()

    assert len(courses) == 3
    assert all(hasattr(course, "name") for course in courses)
    assert all(hasattr(course, "id") for course in courses)


def test_mock_course_service_get_course():
    """Test getting a single course by ID."""
    service = get_course_service()
    courses = service.get_courses()
    first_course_id = courses[0].id

    course = service.get_course(first_course_id)
    assert course.id == first_course_id


def test_mock_course_service_create_course():
    """Test creating a new course."""
    service = get_course_service()
    initial_count = len(service.get_courses())

    new_course = service.create_course("Test Course", cs50_id=999)

    assert new_course.name == "Test Course"
    assert new_course.cs50_id == 999
    assert len(service.get_courses()) == initial_count + 1


def test_mock_course_service_create_course_with_model():
    """Test creating a course with CourseCreate model."""
    service = get_course_service()

    course_data = CourseCreate(name="Advanced Python", cs50_id=200, exercise_ids=["ex1", "ex2"])
    new_course = service.create_course(course_data)

    assert new_course.name == "Advanced Python"
    assert new_course.cs50_id == 200
    assert new_course.exercise_ids == ["ex1", "ex2"]


def test_mock_course_service_delete_course():
    """Test deleting a course."""
    service = get_course_service()
    courses = service.get_courses()
    initial_count = len(courses)
    course_to_delete = courses[0].id

    service.delete_course(course_to_delete)

    assert len(service.get_courses()) == initial_count - 1
    with pytest.raises(ValueError, match="not found"):
        service.get_course(course_to_delete)


def test_mock_enrollment_service_upload_csv():
    """Test mock enrollment CSV upload."""
    from io import BytesIO

    service = get_enrollment_service()

    # Create a mock CSV file
    csv_content = (
        b"email,name\nstudent1@example.com,Student One\nstudent2@example.com,Student Two\n"
    )
    mock_file = BytesIO(csv_content)
    mock_file.name = "test_enrollment.csv"

    result = service.upload_enrollment_csv("course123", mock_file)

    assert result["status"] == "success"
    assert "enrolled_count" in result
    assert result["enrolled_count"] == 2
    assert result["failed_count"] == 0


def test_service_factory_respects_env():
    """Test that service factory respects USE_MOCK_SERVICES environment variable."""
    os.environ["USE_MOCK_SERVICES"] = "true"
    from services.mock_course_service import MockCourseService

    service = get_course_service()
    assert isinstance(service, MockCourseService)
