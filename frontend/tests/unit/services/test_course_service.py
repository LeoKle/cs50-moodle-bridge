import pytest
from unittest.mock import Mock, patch
import requests

from services.course_service import CourseService

pytestmark = pytest.mark.unit


@pytest.fixture
def course_service():
    """Fixture to provide a CourseService instance."""
    return CourseService()


@pytest.fixture
def mock_response():
    """Fixture to create a mock response object."""
    mock = Mock()
    mock.raise_for_status = Mock()
    return mock


def test_course_service_initializes_with_default_url():
    """Test that CourseService initializes with default URL."""
    service = CourseService()
    assert service.base_url == "http://localhost:8000"
    assert service.api_url == "http://localhost:8000/api/v1/courses"


def test_course_service_initializes_with_env_url():
    """Test that CourseService initializes with environment URL."""
    with patch.dict("os.environ", {"BACKEND_URL": "http://example.com:9000"}):
        service = CourseService()
        assert service.base_url == "http://example.com:9000"
        assert service.api_url == "http://example.com:9000/api/v1/courses"


def test_get_courses_returns_list_on_success(course_service, mock_response):
    """Test get_courses returns a list of courses on successful response."""
    mock_courses = [
        {"id": "1", "name": "Course 1", "cs50_id": 50, "exercise_ids": []},
        {"id": "2", "name": "Course 2", "cs50_id": 51, "exercise_ids": []},
    ]
    mock_response.json.return_value = mock_courses

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = course_service.get_courses()

        mock_get.assert_called_once_with(course_service.api_url)
        assert result == mock_courses
        assert len(result) == 2


def test_get_courses_raises_exception_on_request_failure(course_service):
    """Test get_courses raises exception when request fails."""
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError("Connection error")):
        with pytest.raises(Exception) as exc_info:
            course_service.get_courses()

        assert "Failed to fetch courses" in str(exc_info.value)


def test_get_courses_raises_exception_on_http_error(course_service, mock_response):
    """Test get_courses raises exception on HTTP error."""
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(Exception) as exc_info:
            course_service.get_courses()

        assert "Failed to fetch courses" in str(exc_info.value)


def test_get_course_returns_course_on_success(course_service, mock_response):
    """Test get_course returns a single course on successful response."""
    mock_course = {"id": "123", "name": "Test Course", "cs50_id": 50, "exercise_ids": []}
    mock_response.json.return_value = mock_course

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = course_service.get_course("123")

        mock_get.assert_called_once_with(f"{course_service.api_url}/123")
        assert result == mock_course
        assert result["id"] == "123"


def test_get_course_raises_exception_on_request_failure(course_service):
    """Test get_course raises exception when request fails."""
    with patch("requests.get", side_effect=requests.exceptions.Timeout("Timeout")):
        with pytest.raises(Exception) as exc_info:
            course_service.get_course("123")

        assert "Failed to fetch course" in str(exc_info.value)


def test_get_course_raises_exception_on_http_error(course_service, mock_response):
    """Test get_course raises exception on HTTP error."""
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(Exception) as exc_info:
            course_service.get_course("123")

        assert "Failed to fetch course" in str(exc_info.value)


def test_create_course_with_name_only(course_service, mock_response):
    """Test create_course with only name parameter."""
    mock_course = {"id": "1", "name": "New Course", "cs50_id": None, "exercise_ids": []}
    mock_response.json.return_value = mock_course

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = course_service.create_course("New Course")

        mock_post.assert_called_once_with(
            course_service.api_url, json={"name": "New Course"}
        )
        assert result == mock_course
        assert result["name"] == "New Course"
        assert result["cs50_id"] is None


def test_create_course_with_name_and_cs50_id(course_service, mock_response):
    """Test create_course with both name and cs50_id parameters."""
    mock_course = {"id": "1", "name": "New Course", "cs50_id": 100, "exercise_ids": []}
    mock_response.json.return_value = mock_course

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = course_service.create_course("New Course", cs50_id=100)

        mock_post.assert_called_once_with(
            course_service.api_url, json={"name": "New Course", "cs50_id": 100}
        )
        assert result == mock_course
        assert result["cs50_id"] == 100


def test_create_course_with_none_cs50_id(course_service, mock_response):
    """Test create_course with explicitly None cs50_id."""
    mock_course = {"id": "1", "name": "New Course", "cs50_id": None, "exercise_ids": []}
    mock_response.json.return_value = mock_course

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = course_service.create_course("New Course", cs50_id=None)

        mock_post.assert_called_once_with(
            course_service.api_url, json={"name": "New Course"}
        )
        assert result == mock_course


def test_create_course_raises_exception_on_request_failure(course_service):
    """Test create_course raises exception when request fails."""
    with patch("requests.post", side_effect=requests.exceptions.RequestException("Error")):
        with pytest.raises(Exception) as exc_info:
            course_service.create_course("New Course")

        assert "Failed to create course" in str(exc_info.value)


def test_create_course_raises_exception_on_http_error(course_service, mock_response):
    """Test create_course raises exception on HTTP error."""
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("400 Bad Request")

    with patch("requests.post", return_value=mock_response):
        with pytest.raises(Exception) as exc_info:
            course_service.create_course("New Course")

        assert "Failed to create course" in str(exc_info.value)
