"""Test dependency injection container with mock services."""

import pytest

from config.settings import get_app_settings
from dependencies import DependencyContainer
from models.course import CourseCreate

pytestmark = pytest.mark.integration


@pytest.fixture
def mock_container():
    """Fixture to create a container with mock mode enabled."""
    container = DependencyContainer()
    container.config.mode.from_value("mock")
    return container


def test_container_provides_mock_course_service(mock_container):
    """Test that container provides course service with mock repository."""
    service = mock_container.course_service()

    # Initially empty
    courses = service.get_courses()
    assert isinstance(courses, list)

    # Create a course
    new_course = service.create_course("Test Course", cs50_id=42)
    assert hasattr(new_course, "name")
    assert hasattr(new_course, "id")

    # Now should have 1 course
    courses = service.get_courses()
    assert len(courses) == 1


def test_mock_course_service_get_course(mock_container):
    """Test getting a single course by ID."""
    service = mock_container.course_service()

    # Create a course first
    created = service.create_course("Test Course", cs50_id=50)

    # Get it by ID
    course = service.get_course(created.id)
    assert course.id == created.id
    assert course.name == "Test Course"


def test_mock_course_service_create_course(mock_container):
    """Test creating a new course."""
    service = mock_container.course_service()
    initial_count = len(service.get_courses())

    new_course = service.create_course("Test Course", cs50_id=999)

    assert new_course.name == "Test Course"
    assert new_course.cs50_id == 999
    assert len(service.get_courses()) == initial_count + 1


def test_mock_course_service_create_course_with_model(mock_container):
    """Test creating a course with CourseCreate model."""
    service = mock_container.course_service()

    course_data = CourseCreate(name="Advanced Python", cs50_id=200, exercise_ids=["ex1", "ex2"])
    new_course = service.create_course(course_data)

    assert new_course.name == "Advanced Python"
    assert new_course.cs50_id == 200
    assert new_course.exercise_ids == ["ex1", "ex2"]


def test_mock_course_service_delete_course(mock_container):
    """Test deleting a course."""
    service = mock_container.course_service()

    new_course = service.create_course("Course to Delete", cs50_id=123)
    initial_count = len(service.get_courses())
    course_to_delete = new_course.id

    service.delete_course(course_to_delete)

    assert len(service.get_courses()) == initial_count - 1


def test_container_provides_mock_enrollment_service(mock_container):
    """Test that container provides enrollment service with mock repository."""
    from io import BytesIO

    service = mock_container.enrollment_service()

    csv_content = (
        b"Vorname,Nachname,E-Mail-Adresse,Gruppen\n"
        b"Max,Mustermann,max@mail.de,Gruppe A\n"
        b"Anna,Muster,anna@mail.de,Gruppe B\n"
    )
    mock_file = BytesIO(csv_content)
    mock_file.name = "test_enrollment.csv"

    result = service.upload_enrollment_csv("course123", mock_file)

    assert result["status"] == "success"
    assert "enrolled_count" in result


def test_container_mode_selection():
    """Test that container respects mode configuration."""
    container_mock = DependencyContainer()
    container_mock.config.mode.from_value("mock")

    container_prod = DependencyContainer()
    container_prod.config.mode.from_value("production")

    mock_repo = container_mock.course_repository()
    prod_repo = container_prod.course_repository()

    assert type(mock_repo).__name__ == "MockCourseRepository"
    assert type(prod_repo).__name__ == "CourseRepository"


def test_service_uses_injected_repository(mock_container):
    """Test that service receives repository via dependency injection."""
    service = mock_container.course_service()

    course = service.create_course("DI Test Course", cs50_id=42)
    assert course.name == "DI Test Course"

    retrieved = service.get_course(course.id)
    assert retrieved.name == "DI Test Course"
    assert retrieved.cs50_id == 42


def test_settings_integration():
    """Test that app settings can control container mode."""
    settings = get_app_settings()
    expected_mode = "mock" if settings.use_mock_services else "production"

    container = DependencyContainer()
    container.config.mode.from_value(expected_mode)

    service = container.course_service()
    assert service is not None
