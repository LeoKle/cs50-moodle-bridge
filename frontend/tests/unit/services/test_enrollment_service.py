"""Tests for EnrollmentService."""

from io import BytesIO
from unittest.mock import Mock, patch

import pytest
import requests

from services.enrollment_service import EnrollmentService, EnrollmentServiceError

pytestmark = pytest.mark.unit


@pytest.fixture
def enrollment_service():
    """Fixture to provide an EnrollmentService instance."""
    return EnrollmentService()


@pytest.fixture
def mock_response():
    """Fixture to create a mock response object."""
    mock = Mock()
    mock.raise_for_status = Mock()
    return mock


@pytest.fixture
def mock_csv_file():
    """Fixture to create a mock CSV file object with correct German headers."""
    csv_content = (
        b"Vorname,Nachname,E-Mail-Adresse,Gruppen\n"
        b"Max,Mustermann,max.mustermann@mail.de,Programmiergruppe A\n"
    )
    file = BytesIO(csv_content)
    file.name = "test.csv"
    return file


@pytest.fixture
def mock_csv_file_multiple_students():
    """Fixture to create a mock CSV file with multiple students."""
    csv_content = (
        b"Vorname,Nachname,E-Mail-Adresse,Gruppen\n"
        b"Max,Mustermann,max.mustermann@mail.de,Programmiergruppe A \n"
        b"Maxina,Mustermann,maxina.mustermann@mail.de,\n"
        b"Maximum,Mustermann,maximum.mustermann@mail.de,\n"
    )
    file = BytesIO(csv_content)
    file.name = "enrollment.csv"
    return file


@pytest.fixture
def mock_csv_file_empty():
    """Fixture to create a mock CSV file with headers only."""
    csv_content = b"Vorname,Nachname,E-Mail-Adresse,Gruppen\n"
    file = BytesIO(csv_content)
    file.name = "empty.csv"
    return file


def test_enrollment_service_initializes_with_default_url():
    """Test that EnrollmentService initializes with default URL."""
    service = EnrollmentService()
    assert service.base_url == "http://localhost:8000"
    assert service.api_url == "http://localhost:8000/api/v1/enroll"


def test_enrollment_service_initializes_with_env_url():
    """Test that EnrollmentService initializes with environment URL."""
    with patch.dict("os.environ", {"BACKEND_URL": "http://example.com:9000"}):
        service = EnrollmentService()
        assert service.base_url == "http://example.com:9000"
        assert service.api_url == "http://example.com:9000/api/v1/enroll"


def test_upload_enrollment_csv_success(enrollment_service, mock_response, mock_csv_file):
    """Test successful CSV upload."""
    expected_response = {
        "status": "success",
        "course_id": "course-1",
        "enrolled_count": 1,
        "total_students": 1,
    }
    mock_response.json.return_value = expected_response

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == "http://localhost:8000/api/v1/enroll/course-1"

        assert "files" in call_args[1]
        assert "file" in call_args[1]["files"]

        assert call_args[1]["timeout"] == 30

        assert result == expected_response
        mock_response.raise_for_status.assert_called_once()


def test_upload_enrollment_csv_http_error(enrollment_service, mock_csv_file):
    """Test that HTTP errors raise EnrollmentServiceError."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with patch("requests.post", return_value=mock_response):
        with pytest.raises(EnrollmentServiceError) as exc_info:
            enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

        assert "Failed to upload enrollment CSV" in str(exc_info.value)


def test_upload_enrollment_csv_connection_error(enrollment_service, mock_csv_file):
    """Test that connection errors raise EnrollmentServiceError."""
    with patch("requests.post", side_effect=requests.exceptions.ConnectionError("No network")):
        with pytest.raises(EnrollmentServiceError) as exc_info:
            enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

        assert "Failed to upload enrollment CSV" in str(exc_info.value)


def test_upload_enrollment_csv_timeout_error(enrollment_service, mock_csv_file):
    """Test that timeout errors raise EnrollmentServiceError."""
    with patch("requests.post", side_effect=requests.exceptions.Timeout("Timeout")):
        with pytest.raises(EnrollmentServiceError) as exc_info:
            enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

        assert "Failed to upload enrollment CSV" in str(exc_info.value)


def test_upload_enrollment_csv_request_exception(enrollment_service, mock_csv_file):
    """Test that general request exceptions raise EnrollmentServiceError."""
    with patch("requests.post", side_effect=requests.exceptions.RequestException("Error")):
        with pytest.raises(EnrollmentServiceError) as exc_info:
            enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

        assert "Failed to upload enrollment CSV" in str(exc_info.value)


def test_upload_enrollment_csv_with_different_course_id(
    enrollment_service, mock_response, mock_csv_file
):
    """Test CSV upload with different course ID."""
    expected_response = {"status": "success", "course_id": "test-course-123"}
    mock_response.json.return_value = expected_response

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = enrollment_service.upload_enrollment_csv("test-course-123", mock_csv_file)

        call_args = mock_post.call_args
        assert call_args[0][0] == "http://localhost:8000/api/v1/enroll/test-course-123"
        assert result == expected_response


def test_upload_enrollment_csv_multiple_students(
    enrollment_service, mock_response, mock_csv_file_multiple_students
):
    """Test CSV upload with multiple students."""
    expected_response = {
        "status": "success",
        "course_id": "course-1",
        "enrolled_count": 3,
        "total_students": 3,
    }
    mock_response.json.return_value = expected_response


def test_upload_enrollment_csv_empty_file(enrollment_service, mock_response, mock_csv_file_empty):
    """Test CSV upload with empty file (headers only)."""
    expected_response = {
        "status": "success",
        "course_id": "course-1",
        "enrolled_count": 0,
        "total_students": 0,
    }
    mock_response.json.return_value = expected_response


def test_upload_enrollment_csv_with_special_characters_in_course_id(
    enrollment_service, mock_response, mock_csv_file
):
    """Test CSV upload with special characters in course ID."""
    course_id = "course-2024-winter-semester"
    expected_response = {"status": "success", "course_id": course_id}
    mock_response.json.return_value = expected_response

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = enrollment_service.upload_enrollment_csv(course_id, mock_csv_file)

        call_args = mock_post.call_args
        assert call_args[0][0] == f"http://localhost:8000/api/v1/enroll/{course_id}"
        assert result == expected_response


def test_upload_enrollment_csv_verifies_file_metadata(
    enrollment_service, mock_response, mock_csv_file
):
    """Test that file metadata is correctly passed."""
    expected_response = {"status": "success"}
    mock_response.json.return_value = expected_response

    with patch("requests.post", return_value=mock_response) as mock_post:
        enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

        call_args = mock_post.call_args
        files_param = call_args[1]["files"]
        assert files_param["file"][0] == "test.csv"
        assert files_param["file"][2] == "text/csv"


def test_upload_enrollment_csv_partial_enrollment(
    enrollment_service, mock_response, mock_csv_file_multiple_students
):
    """Test CSV upload where only some students were enrolled (e.g., some duplicates)."""
    expected_response = {
        "status": "partial",
        "course_id": "course-1",
        "enrolled_count": 2,
        "total_students": 3,
        "skipped": 1,
    }
    mock_response.json.return_value = expected_response

    with patch("requests.post", return_value=mock_response):
        result = enrollment_service.upload_enrollment_csv(
            "course-1", mock_csv_file_multiple_students
        )

        assert result["status"] == "partial"
        assert result["enrolled_count"] == 2
        assert result["total_students"] == 3
        assert result["skipped"] == 1
