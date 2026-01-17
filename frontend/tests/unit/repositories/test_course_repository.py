"""Integration tests for CourseRepository HTTP communication."""

from unittest.mock import Mock, patch

import httpx
import pytest

from models.course import CourseCreate, CourseOut, CourseUpdate
from repositories.course_repository import CourseRepository, CourseRepositoryError

pytestmark = pytest.mark.unit


@pytest.fixture
def course_repository():
    """Fixture to provide a CourseRepository instance."""
    return CourseRepository()


@pytest.fixture
def mock_httpx_client():
    """Fixture to create a mock HTTPX client."""
    mock = Mock(spec=httpx.Client)
    return mock


@pytest.fixture
def sample_course_data():
    """Fixture providing sample course data."""
    return {
        "id": "507f1f77bcf86cd799439011",
        "name": "Python Programming",
        "cs50_id": 50,
        "exercise_ids": ["ex1", "ex2"],
    }


def test_get_all_returns_courses(course_repository, mock_httpx_client, sample_course_data):
    """Test get_all successfully fetches courses."""
    mock_response = Mock()
    mock_response.json.return_value = [sample_course_data]
    mock_response.raise_for_status = Mock()
    mock_httpx_client.get.return_value = mock_response

    with patch.object(course_repository, "_client", mock_httpx_client):
        result = course_repository.get_all()

    assert len(result) == 1
    assert isinstance(result[0], CourseOut)
    assert result[0].name == "Python Programming"
    assert result[0].cs50_id == 50
    mock_httpx_client.get.assert_called_once()


def test_get_all_raises_error_on_http_failure(course_repository, mock_httpx_client):
    """Test get_all raises CourseRepositoryError on HTTP error."""
    mock_httpx_client.get.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=Mock(), response=Mock()
    )

    with (
        patch.object(course_repository, "_client", mock_httpx_client),
        pytest.raises(CourseRepositoryError) as exc_info,
    ):
        course_repository.get_all()

    assert "Failed to fetch courses" in str(exc_info.value)


def test_get_by_id_returns_course(course_repository, mock_httpx_client, sample_course_data):
    """Test get_by_id successfully fetches a single course."""
    mock_response = Mock()
    mock_response.json.return_value = sample_course_data
    mock_response.raise_for_status = Mock()
    mock_httpx_client.get.return_value = mock_response

    with patch.object(course_repository, "_client", mock_httpx_client):
        result = course_repository.get_by_id("507f1f77bcf86cd799439011")

    assert isinstance(result, CourseOut)
    assert result.id == "507f1f77bcf86cd799439011"
    assert result.name == "Python Programming"
    mock_httpx_client.get.assert_called_once()


def test_get_by_id_raises_error_on_not_found(course_repository, mock_httpx_client):
    """Test get_by_id raises CourseRepositoryError when course not found."""
    mock_httpx_client.get.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=Mock(), response=Mock()
    )

    with (
        patch.object(course_repository, "_client", mock_httpx_client),
        pytest.raises(CourseRepositoryError) as exc_info,
    ):
        course_repository.get_by_id("nonexistent")

    assert "Failed to fetch course" in str(exc_info.value)


def test_create_course_success(course_repository, mock_httpx_client, sample_course_data):
    """Test create successfully creates a course."""
    course_create = CourseCreate(name="Python Programming", cs50_id=50, exercise_ids=["ex1"])

    mock_response = Mock()
    mock_response.json.return_value = sample_course_data
    mock_response.raise_for_status = Mock()
    mock_httpx_client.post.return_value = mock_response

    with patch.object(course_repository, "_client", mock_httpx_client):
        result = course_repository.create(course_create)

    assert isinstance(result, CourseOut)
    assert result.name == "Python Programming"
    mock_httpx_client.post.assert_called_once()


def test_create_course_raises_error_on_failure(course_repository, mock_httpx_client):
    """Test create raises CourseRepositoryError on HTTP error."""
    course_create = CourseCreate(name="Test Course", cs50_id=50)

    mock_httpx_client.post.side_effect = httpx.HTTPStatusError(
        "400 Bad Request", request=Mock(), response=Mock()
    )

    with (
        patch.object(course_repository, "_client", mock_httpx_client),
        pytest.raises(CourseRepositoryError) as exc_info,
    ):
        course_repository.create(course_create)

    assert "Failed to create course" in str(exc_info.value)


def test_update_course_success(course_repository, mock_httpx_client, sample_course_data):
    """Test update successfully updates a course."""
    course_update = CourseUpdate(name="Advanced Python")

    updated_data = sample_course_data.copy()
    updated_data["name"] = "Advanced Python"

    mock_response = Mock()
    mock_response.json.return_value = updated_data
    mock_response.raise_for_status = Mock()
    mock_httpx_client.patch.return_value = mock_response

    with patch.object(course_repository, "_client", mock_httpx_client):
        result = course_repository.update("507f1f77bcf86cd799439011", course_update)

    assert isinstance(result, CourseOut)
    assert result.name == "Advanced Python"
    mock_httpx_client.patch.assert_called_once()


def test_update_course_raises_error_on_not_found(course_repository, mock_httpx_client):
    """Test update raises CourseRepositoryError when course not found."""
    course_update = CourseUpdate(name="Updated Name")

    mock_httpx_client.patch.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=Mock(), response=Mock()
    )

    with (
        patch.object(course_repository, "_client", mock_httpx_client),
        pytest.raises(CourseRepositoryError) as exc_info,
    ):
        course_repository.update("nonexistent", course_update)

    assert "Failed to update course" in str(exc_info.value)


def test_delete_course_success(course_repository, mock_httpx_client):
    """Test delete successfully deletes a course."""
    mock_response = Mock()
    mock_response.status_code = 204
    mock_response.raise_for_status = Mock()
    mock_httpx_client.delete.return_value = mock_response

    with patch.object(course_repository, "_client", mock_httpx_client):
        result = course_repository.delete("507f1f77bcf86cd799439011")

    assert result is True
    mock_httpx_client.delete.assert_called_once()


def test_delete_course_raises_error_on_not_found(course_repository, mock_httpx_client):
    """Test delete raises CourseRepositoryError when course not found."""
    mock_httpx_client.delete.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=Mock(), response=Mock()
    )

    with (
        patch.object(course_repository, "_client", mock_httpx_client),
        pytest.raises(CourseRepositoryError) as exc_info,
    ):
        course_repository.delete("nonexistent")

    assert "Failed to delete course" in str(exc_info.value)


def test_repository_uses_correct_base_url():
    """Test repository initializes with correct base URL from settings."""
    repo = CourseRepository()
    assert repo._client.base_url is not None


def test_repository_uses_correct_api_path():
    """Test repository constructs correct API path."""
    repo = CourseRepository()
    assert repo._api_path == "/api/v1/courses"
