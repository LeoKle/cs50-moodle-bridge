"""Tests for EnrollmentService with repository pattern."""

from io import BytesIO

import pytest

from services.enrollment_service import EnrollmentService, EnrollmentServiceError
from tests.mocks.repositories.enrollment_repository_mock import (
    MockEnrollmentRepository,
    MockEnrollmentRepositoryError,
)

pytestmark = pytest.mark.unit


@pytest.fixture
def mock_repository():
    """Fixture to provide a MockEnrollmentRepository instance."""
    return MockEnrollmentRepository()


@pytest.fixture
def enrollment_service(mock_repository):
    """Fixture to provide an EnrollmentService instance with mock repository."""
    return EnrollmentService(repository=mock_repository)


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


def test_upload_enrollment_csv_success(enrollment_service, mock_repository, mock_csv_file):
    """Test successful CSV upload."""
    result = enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

    assert result["status"] == "success"
    assert result["course_id"] == "course-1"
    assert "enrolled_count" in result
    assert "total_students" in result

    history = mock_repository.get_upload_history()
    assert len(history) == 1
    assert history[0]["course_id"] == "course-1"
    assert history[0]["filename"] == "test.csv"


def test_upload_enrollment_csv_validates_course_id(enrollment_service, mock_csv_file):
    """Test that empty course ID raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        enrollment_service.upload_enrollment_csv("", mock_csv_file)

    assert "Course ID cannot be empty" in str(exc_info.value)


def test_upload_enrollment_csv_validates_whitespace_course_id(enrollment_service, mock_csv_file):
    """Test that whitespace-only course ID raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        enrollment_service.upload_enrollment_csv("   ", mock_csv_file)

    assert "Course ID cannot be empty" in str(exc_info.value)


def test_upload_enrollment_csv_validates_file(enrollment_service):
    """Test that missing file raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        enrollment_service.upload_enrollment_csv("course-1", None)

    assert "File is required" in str(exc_info.value)


def test_upload_enrollment_csv_raises_service_error_on_repository_failure(
    enrollment_service, mock_repository, mock_csv_file
):
    """Test that repository errors are wrapped in EnrollmentServiceError."""

    def raise_error(course_id, file):
        msg = "Upload failed"
        raise MockEnrollmentRepositoryError(msg)

    mock_repository.upload_csv = raise_error

    with pytest.raises(EnrollmentServiceError) as exc_info:
        enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

    assert "Failed to upload enrollment CSV" in str(exc_info.value)


def test_upload_enrollment_csv_with_different_course_id(
    enrollment_service, mock_repository, mock_csv_file
):
    """Test CSV upload with different course ID."""
    result = enrollment_service.upload_enrollment_csv("test-course-123", mock_csv_file)

    assert result["status"] == "success"
    assert result["course_id"] == "test-course-123"

    history = mock_repository.get_upload_history()
    assert history[0]["course_id"] == "test-course-123"


def test_upload_enrollment_csv_multiple_students(
    enrollment_service, mock_repository, mock_csv_file_multiple_students
):
    """Test CSV upload with multiple students."""
    result = enrollment_service.upload_enrollment_csv("course-1", mock_csv_file_multiple_students)

    assert result["status"] == "success"
    assert result["course_id"] == "course-1"

    history = mock_repository.get_upload_history()
    assert history[0]["filename"] == "enrollment.csv"


def test_upload_enrollment_csv_empty_file(enrollment_service, mock_repository, mock_csv_file_empty):
    """Test CSV upload with empty file (headers only)."""
    result = enrollment_service.upload_enrollment_csv("course-1", mock_csv_file_empty)

    assert result["status"] == "success"
    assert result["course_id"] == "course-1"

    history = mock_repository.get_upload_history()
    assert history[0]["filename"] == "empty.csv"


def test_upload_enrollment_csv_with_special_characters_in_course_id(
    enrollment_service, mock_repository, mock_csv_file
):
    """Test CSV upload with special characters in course ID."""
    course_id = "course-2024-winter-semester"
    result = enrollment_service.upload_enrollment_csv(course_id, mock_csv_file)

    assert result["status"] == "success"
    assert result["course_id"] == course_id

    history = mock_repository.get_upload_history()
    assert history[0]["course_id"] == course_id


def test_upload_enrollment_csv_preserves_file_metadata(
    enrollment_service, mock_repository, mock_csv_file
):
    """Test that file metadata is correctly passed to repository."""
    enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

    history = mock_repository.get_upload_history()
    assert history[0]["filename"] == "test.csv"


def test_multiple_uploads_tracked(enrollment_service, mock_repository, mock_csv_file):
    """Test that multiple uploads are tracked in the repository."""
    enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

    mock_csv_file.seek(0)
    enrollment_service.upload_enrollment_csv("course-2", mock_csv_file)

    history = mock_repository.get_upload_history()
    assert len(history) == 2
    assert history[0]["course_id"] == "course-1"
    assert history[1]["course_id"] == "course-2"


def test_service_uses_repository_methods(enrollment_service, mock_repository, mock_csv_file):
    """Test that service properly delegates to repository methods."""
    result = enrollment_service.upload_enrollment_csv("course-1", mock_csv_file)

    assert result is not None
    assert isinstance(result, dict)

    history = mock_repository.get_upload_history()
    assert len(history) == 1
