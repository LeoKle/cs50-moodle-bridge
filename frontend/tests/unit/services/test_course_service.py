"""Tests for CourseService with repository pattern."""

import pytest

from models.course import CourseCreate, CourseOut, CourseUpdate
from services.course_service import CourseService, CourseServiceError
from tests.mocks.repositories.course_repository_mock import (
    MockCourseRepository,
    MockCourseRepositoryError,
)

pytestmark = pytest.mark.unit


@pytest.fixture
def mock_repository():
    """Fixture to provide a MockCourseRepository instance."""
    return MockCourseRepository()


@pytest.fixture
def course_service(mock_repository):
    """Fixture to provide a CourseService instance with mock repository."""
    return CourseService(repository=mock_repository)


@pytest.fixture
def sample_courses():
    """Fixture to provide sample course data."""
    return [
        CourseOut(id="1", name="Python Programming", cs50_id=50, exercise_ids=[]),
        CourseOut(id="2", name="Advanced Python", cs50_id=51, exercise_ids=["ex1", "ex2"]),
        CourseOut(id="3", name="Data Structures", cs50_id=52, exercise_ids=[]),
    ]


def test_get_courses_returns_empty_list_when_no_courses(course_service):
    """Test get_courses returns empty list when repository has no data."""
    result = course_service.get_courses()
    assert result == []
    assert isinstance(result, list)


def test_get_courses_returns_sorted_list(course_service, mock_repository, sample_courses):
    """Test get_courses returns courses sorted by name."""
    mock_repository.seed_data(sample_courses)

    result = course_service.get_courses()

    assert len(result) == 3
    assert result[0].name == "Advanced Python"
    assert result[1].name == "Data Structures"
    assert result[2].name == "Python Programming"


def test_get_courses_raises_service_error_on_repository_failure(course_service, mock_repository):
    """Test get_courses raises CourseServiceError when repository fails."""

    def raise_error():
        msg = "Database error"
        raise MockCourseRepositoryError(msg)

    mock_repository.get_all = raise_error

    with pytest.raises(CourseServiceError) as exc_info:
        course_service.get_courses()

    assert "Failed to fetch courses" in str(exc_info.value)


def test_get_course_returns_course_by_id(course_service, mock_repository, sample_courses):
    """Test get_course returns a single course by ID."""
    mock_repository.seed_data(sample_courses)

    result = course_service.get_course("2")

    assert result.id == "2"
    assert result.name == "Advanced Python"
    assert result.cs50_id == 51
    assert result.exercise_ids == ["ex1", "ex2"]


def test_get_course_raises_error_when_not_found(course_service):
    """Test get_course raises CourseServiceError when course doesn't exist."""
    with pytest.raises(CourseServiceError) as exc_info:
        course_service.get_course("nonexistent")

    assert "Failed to fetch course" in str(exc_info.value)


def test_get_course_raises_service_error_on_repository_failure(course_service, mock_repository):
    """Test get_course raises CourseServiceError when repository fails."""

    def raise_error(course_id):
        msg = "Database connection lost"
        raise MockCourseRepositoryError(msg)

    mock_repository.get_by_id = raise_error

    with pytest.raises(CourseServiceError) as exc_info:
        course_service.get_course("123")

    assert "Failed to fetch course" in str(exc_info.value)


def test_create_course_with_name_string(course_service):
    """Test create_course with only name parameter as string."""
    result = course_service.create_course("New Course")

    assert result.name == "New Course"
    assert result.id is not None
    assert result.cs50_id is None
    assert result.exercise_ids == []


def test_create_course_with_name_and_cs50_id(course_service):
    """Test create_course with both name and cs50_id parameters."""
    result = course_service.create_course("Advanced Course", cs50_id=100)

    assert result.name == "Advanced Course"
    assert result.cs50_id == 100
    assert result.id is not None


def test_create_course_with_course_create_object(course_service):
    """Test create_course with CourseCreate object."""
    course_data = CourseCreate(name="Test Course", cs50_id=50, exercise_ids=["ex1", "ex2", "ex3"])

    result = course_service.create_course(course_data)

    assert result.name == "Test Course"
    assert result.cs50_id == 50
    assert result.exercise_ids == ["ex1", "ex2", "ex3"]


def test_create_course_validates_empty_name(course_service):
    """Test create_course raises ValueError when name is empty."""
    with pytest.raises(ValueError) as exc_info:
        course_service.create_course("")

    # Pydantic validation error for empty string
    assert "String should have at least 1 character" in str(exc_info.value)


def test_create_course_validates_whitespace_name(course_service):
    """Test create_course raises ValueError when name is only whitespace."""
    with pytest.raises(ValueError) as exc_info:
        course_service.create_course("   ")

    assert "Course name cannot be empty" in str(exc_info.value)


def test_create_course_raises_service_error_on_repository_failure(course_service, mock_repository):
    """Test create_course raises CourseServiceError when repository fails."""

    def raise_error(course):
        msg = "Database write error"
        raise MockCourseRepositoryError(msg)

    mock_repository.create = raise_error

    with pytest.raises(CourseServiceError) as exc_info:
        course_service.create_course("New Course")

    assert "Failed to create course" in str(exc_info.value)


def test_delete_course_removes_course(course_service, mock_repository, sample_courses):
    """Test delete_course successfully deletes a course."""
    mock_repository.seed_data(sample_courses)

    assert len(mock_repository.get_all()) == 3

    course_service.delete_course("2")

    courses = mock_repository.get_all()
    assert len(courses) == 2
    assert all(c.id != "2" for c in courses)


def test_delete_course_raises_error_when_not_found(course_service):
    """Test delete_course raises CourseServiceError when course doesn't exist."""
    with pytest.raises(CourseServiceError) as exc_info:
        course_service.delete_course("nonexistent")

    assert "Failed to delete course" in str(exc_info.value)


def test_delete_course_raises_service_error_on_repository_failure(course_service, mock_repository):
    """Test delete_course raises CourseServiceError when repository fails."""

    def raise_error(course_id):
        msg = "Database delete error"
        raise MockCourseRepositoryError(msg)

    mock_repository.delete = raise_error

    with pytest.raises(CourseServiceError) as exc_info:
        course_service.delete_course("123")

    assert "Failed to delete course" in str(exc_info.value)


def test_update_course_updates_name(course_service, mock_repository, sample_courses):
    """Test update_course successfully updates course name."""
    mock_repository.seed_data(sample_courses)

    update_data = CourseUpdate(name="Updated Python Programming")
    result = course_service.update_course("1", update_data)

    assert result.id == "1"
    assert result.name == "Updated Python Programming"
    assert result.cs50_id == 50  # Unchanged
    assert result.exercise_ids == []  # Unchanged


def test_update_course_updates_cs50_id(course_service, mock_repository, sample_courses):
    """Test update_course successfully updates CS50 ID."""
    mock_repository.seed_data(sample_courses)

    update_data = CourseUpdate(cs50_id=999)
    result = course_service.update_course("2", update_data)

    assert result.id == "2"
    assert result.name == "Advanced Python"  # Unchanged
    assert result.cs50_id == 999
    assert result.exercise_ids == ["ex1", "ex2"]  # Unchanged


def test_update_course_updates_exercise_ids(course_service, mock_repository, sample_courses):
    """Test update_course successfully updates exercise IDs."""
    mock_repository.seed_data(sample_courses)

    update_data = CourseUpdate(exercise_ids=["new1", "new2", "new3"])
    result = course_service.update_course("3", update_data)

    assert result.id == "3"
    assert result.name == "Data Structures"  # Unchanged
    assert result.cs50_id == 52  # Unchanged
    assert result.exercise_ids == ["new1", "new2", "new3"]


def test_update_course_updates_multiple_fields(course_service, mock_repository, sample_courses):
    """Test update_course successfully updates multiple fields at once."""
    mock_repository.seed_data(sample_courses)

    update_data = CourseUpdate(
        name="Completely New Name",
        cs50_id=777,
        exercise_ids=["a", "b", "c"],
    )
    result = course_service.update_course("1", update_data)

    assert result.id == "1"
    assert result.name == "Completely New Name"
    assert result.cs50_id == 777
    assert result.exercise_ids == ["a", "b", "c"]


def test_update_course_validates_empty_name(course_service, mock_repository, sample_courses):
    """Test update_course raises ValueError when name is empty."""
    mock_repository.seed_data(sample_courses)

    # Pydantic will catch this during model validation
    with pytest.raises(ValueError) as exc_info:
        CourseUpdate(name="")

    assert "String should have at least 1 character" in str(exc_info.value)


def test_update_course_validates_whitespace_name(course_service, mock_repository, sample_courses):
    """Test update_course raises ValueError when name is only whitespace."""
    mock_repository.seed_data(sample_courses)

    update_data = CourseUpdate(name="   ")

    with pytest.raises(ValueError) as exc_info:
        course_service.update_course("1", update_data)

    assert "Course name cannot be empty" in str(exc_info.value)


def test_update_course_raises_error_when_not_found(course_service):
    """Test update_course raises CourseServiceError when course doesn't exist."""
    update_data = CourseUpdate(name="New Name")

    with pytest.raises(CourseServiceError) as exc_info:
        course_service.update_course("nonexistent", update_data)

    assert "Failed to update course" in str(exc_info.value)


def test_update_course_raises_service_error_on_repository_failure(
    course_service, mock_repository, sample_courses
):
    """Test update_course raises CourseServiceError when repository fails."""
    mock_repository.seed_data(sample_courses)

    def raise_error(course_id, course):
        msg = "Database update error"
        raise MockCourseRepositoryError(msg)

    mock_repository.update = raise_error

    update_data = CourseUpdate(name="New Name")

    with pytest.raises(CourseServiceError) as exc_info:
        course_service.update_course("1", update_data)

    assert "Failed to update course" in str(exc_info.value)


def test_service_uses_repository_methods(course_service, mock_repository):
    """Test that service properly delegates to repository methods."""
    course = course_service.create_course("Test Course", cs50_id=42)

    all_courses = mock_repository.get_all()
    assert len(all_courses) == 1
    assert all_courses[0].name == "Test Course"

    retrieved = course_service.get_course(course.id)
    assert retrieved.name == "Test Course"
    assert retrieved.cs50_id == 42
