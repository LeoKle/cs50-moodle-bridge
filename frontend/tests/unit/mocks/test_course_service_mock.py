import pytest

from tests.mocks.services.course_service_mock import MockCourseService

pytestmark = pytest.mark.unit


@pytest.fixture
def mock_service():
    """Fixture to provide a fresh MockCourseService instance."""
    return MockCourseService()


def test_mock_service_initializes_empty(mock_service):
    """Test that MockCourseService initializes with no courses."""
    courses = mock_service.get_courses()
    assert courses == []


def test_create_course_adds_course(mock_service):
    """Test that create_course adds a course to the mock data."""
    course = mock_service.create_course("Test Course", cs50_id=50)

    assert course["name"] == "Test Course"
    assert course["cs50_id"] == 50
    assert course["exercise_ids"] == []
    assert "id" in course


def test_create_course_generates_unique_ids(mock_service):
    """Test that create_course generates unique IDs for each course."""
    course1 = mock_service.create_course("Course 1")
    course2 = mock_service.create_course("Course 2")

    assert course1["id"] != course2["id"]


def test_create_course_without_cs50_id(mock_service):
    """Test that create_course works without cs50_id."""
    course = mock_service.create_course("Test Course")

    assert course["name"] == "Test Course"
    assert course["cs50_id"] is None


def test_get_courses_returns_all_courses(mock_service):
    """Test that get_courses returns all created courses."""
    mock_service.create_course("Course 1", cs50_id=10)
    mock_service.create_course("Course 2", cs50_id=20)

    courses = mock_service.get_courses()

    assert len(courses) == 2
    assert {c["name"] for c in courses} == {"Course 1", "Course 2"}


def test_get_course_returns_existing_course(mock_service):
    """Test that get_course returns a course by ID."""
    created = mock_service.create_course("Test Course", cs50_id=50)

    result = mock_service.get_course(created["id"])

    assert result["id"] == created["id"]
    assert result["name"] == "Test Course"
    assert result["cs50_id"] == 50


def test_get_course_raises_exception_for_nonexistent_id(mock_service):
    """Test that get_course raises exception for non-existent ID."""
    with pytest.raises(Exception) as exc_info:
        mock_service.get_course("nonexistent")

    assert "not found" in str(exc_info.value)


def test_reset_clears_all_data(mock_service):
    """Test that reset clears all mock data."""
    mock_service.create_course("Course 1")
    mock_service.create_course("Course 2")

    mock_service.reset()

    assert mock_service.get_courses() == []


def test_reset_resets_id_counter(mock_service):
    """Test that reset resets the ID counter."""
    course1 = mock_service.create_course("Course 1")
    mock_service.reset()
    course2 = mock_service.create_course("Course 2")

    assert course1["id"] == course2["id"] == "1"


def test_delete_course_removes_course(mock_service):
    """Test that delete_course removes a course from the mock data."""
    course = mock_service.create_course("Test Course", cs50_id=50)
    course_id = course["id"]

    mock_service.delete_course(course_id)

    assert mock_service.get_courses() == []


def test_delete_course_raises_exception_for_nonexistent_id(mock_service):
    """Test that delete_course raises exception for non-existent ID."""
    with pytest.raises(Exception) as exc_info:
        mock_service.delete_course("nonexistent")

    assert "not found" in str(exc_info.value)


def test_delete_course_removes_specific_course(mock_service):
    """Test that delete_course removes only the specified course."""
    course1 = mock_service.create_course("Course 1", cs50_id=10)
    course2 = mock_service.create_course("Course 2", cs50_id=20)

    mock_service.delete_course(course1["id"])

    courses = mock_service.get_courses()
    assert len(courses) == 1
    assert courses[0]["id"] == course2["id"]
    assert courses[0]["name"] == "Course 2"
