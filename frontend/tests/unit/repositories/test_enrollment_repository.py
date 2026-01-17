"""Integration tests for EnrollmentRepository HTTP communication."""

from io import BytesIO
from unittest.mock import Mock, patch

import httpx
import pytest

from repositories.enrollment_repository import (
    EnrollmentRepository,
    EnrollmentRepositoryError,
)

pytestmark = pytest.mark.unit


@pytest.fixture
def enrollment_repository():
    """Fixture to provide an EnrollmentRepository instance."""
    return EnrollmentRepository()


@pytest.fixture
def mock_httpx_client():
    """Fixture to create a mock HTTPX client."""
    mock = Mock(spec=httpx.Client)
    return mock


@pytest.fixture
def mock_csv_file():
    """Fixture to create a mock CSV file object."""
    csv_content = (
        b"Vorname,Nachname,E-Mail-Adresse,Gruppen\n"
        b"Max,Mustermann,max.mustermann@mail.de,Programmiergruppe A\n"
    )
    file = BytesIO(csv_content)
    file.name = "test.csv"
    return file


def test_upload_csv_success(enrollment_repository, mock_httpx_client, mock_csv_file):
    """Test upload_csv successfully uploads a file."""
    expected_response = {
        "status": "success",
        "course_id": "course-1",
        "enrolled_count": 1,
        "total_students": 1,
    }

    mock_response = Mock()
    mock_response.json.return_value = expected_response
    mock_response.raise_for_status = Mock()
    mock_httpx_client.post.return_value = mock_response

    with patch.object(enrollment_repository, "_client", mock_httpx_client):
        result = enrollment_repository.upload_csv("course-1", mock_csv_file)

    assert result == expected_response
    assert result["status"] == "success"
    assert result["course_id"] == "course-1"
    mock_httpx_client.post.assert_called_once()


def test_upload_csv_sends_correct_file_format(
    enrollment_repository, mock_httpx_client, mock_csv_file
):
    """Test upload_csv sends file with correct format."""
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}
    mock_response.raise_for_status = Mock()
    mock_httpx_client.post.return_value = mock_response

    with patch.object(enrollment_repository, "_client", mock_httpx_client):
        enrollment_repository.upload_csv("course-1", mock_csv_file)

    call_args = mock_httpx_client.post.call_args
    assert call_args is not None
    assert "files" in call_args[1]
    files_param = call_args[1]["files"]
    assert "file" in files_param
    assert files_param["file"][0] == "test.csv"
    assert files_param["file"][2] == "text/csv"


def test_upload_csv_uses_correct_endpoint(enrollment_repository, mock_httpx_client, mock_csv_file):
    """Test upload_csv uses correct API endpoint."""
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}
    mock_response.raise_for_status = Mock()
    mock_httpx_client.post.return_value = mock_response

    with patch.object(enrollment_repository, "_client", mock_httpx_client):
        enrollment_repository.upload_csv("test-course-123", mock_csv_file)

    call_args = mock_httpx_client.post.call_args
    assert call_args[0][0] == "/api/v1/enroll/test-course-123"


def test_upload_csv_raises_error_on_http_failure(
    enrollment_repository, mock_httpx_client, mock_csv_file
):
    """Test upload_csv raises EnrollmentRepositoryError on HTTP error."""
    mock_httpx_client.post.side_effect = httpx.HTTPStatusError(
        "400 Bad Request", request=Mock(), response=Mock()
    )

    with (
        patch.object(enrollment_repository, "_client", mock_httpx_client),
        pytest.raises(EnrollmentRepositoryError) as exc_info,
    ):
        enrollment_repository.upload_csv("course-1", mock_csv_file)

    assert "Failed to upload enrollment CSV" in str(exc_info.value)


def test_upload_csv_raises_error_on_server_error(
    enrollment_repository, mock_httpx_client, mock_csv_file
):
    """Test upload_csv raises EnrollmentRepositoryError on server error."""
    mock_httpx_client.post.side_effect = httpx.HTTPStatusError(
        "500 Internal Server Error", request=Mock(), response=Mock()
    )

    with (
        patch.object(enrollment_repository, "_client", mock_httpx_client),
        pytest.raises(EnrollmentRepositoryError) as exc_info,
    ):
        enrollment_repository.upload_csv("course-1", mock_csv_file)

    assert "Failed to upload enrollment CSV" in str(exc_info.value)


def test_repository_uses_correct_base_url():
    """Test repository initializes with correct base URL from settings."""
    repo = EnrollmentRepository()
    assert repo._client.base_url is not None


def test_repository_uses_correct_api_path():
    """Test repository constructs correct API path."""
    repo = EnrollmentRepository()
    assert repo._api_path == "/api/v1/enroll"


def test_upload_csv_handles_partial_success(
    enrollment_repository, mock_httpx_client, mock_csv_file
):
    """Test upload_csv handles partial enrollment success."""
    expected_response = {
        "status": "partial",
        "course_id": "course-1",
        "enrolled_count": 2,
        "total_students": 3,
        "skipped": 1,
    }

    mock_response = Mock()
    mock_response.json.return_value = expected_response
    mock_response.raise_for_status = Mock()
    mock_httpx_client.post.return_value = mock_response

    with patch.object(enrollment_repository, "_client", mock_httpx_client):
        result = enrollment_repository.upload_csv("course-1", mock_csv_file)

    assert result["status"] == "partial"
    assert result["skipped"] == 1
