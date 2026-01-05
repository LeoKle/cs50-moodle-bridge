import io
from unittest.mock import Mock

import pytest

from exceptions.exceptions import CourseDoesNotExistException, InvalidCsvFormat
from models.course import Course
from models.student import StudentModel
from services.enrollment import EnrollmentService
from tests.mocks.repositories.course_repository_mock import MockCourseRepository
from tests.mocks.repositories.student_repository_mock import MockStudentRepository

pytestmark = pytest.mark.unit


@pytest.fixture
def enrollment_context():
    student_repo = MockStudentRepository()
    course_repo = MockCourseRepository()
    enrollment_repo = Mock()

    course_repo.create(Course(id="course_id", name="Course name", cs50_id=50))

    service = EnrollmentService(
        student_repo,
        course_repo,
        enrollment_repo,
    )

    return {
        "service": service,
        "student_repo": student_repo,
        "enrollment_repo": enrollment_repo,
    }


def test_import_creates_student_and_enrollment(enrollment_context):
    service = enrollment_context["service"]
    student_repo = enrollment_context["student_repo"]

    csv_content = """Vorname,Nachname,E-Mail-Adresse
John,Doe,john.doe@example.com
"""
    csv_file = io.BytesIO(csv_content.encode())

    result = service.import_students_from_csv("course_id", csv_file)

    assert result.students_created == 1
    assert result.enrollments_created == 1
    assert result.rows_skipped == 0

    assert student_repo.get_by_email("john.doe@example.com") is not None


def test_existing_student_is_not_created_again(enrollment_context):
    service = enrollment_context["service"]
    student_repo = enrollment_context["student_repo"]

    student_repo.create(StudentModel(email="john.doe@example.com", name="John Doe"))

    csv_content = """Vorname,Nachname,E-Mail-Adresse
John,Doe,john.doe@example.com
"""
    csv_file = io.BytesIO(csv_content.encode())

    result = service.import_students_from_csv("course_id", csv_file)

    assert result.students_created == 0
    assert result.enrollments_created == 1


def test_rows_without_email_are_skipped(enrollment_context):
    service = enrollment_context["service"]
    student_repo = enrollment_context["student_repo"]

    csv_content = """Vorname,Nachname,E-Mail-Adresse
John,Doe,
Jane,Doe,jane@example.com
"""
    csv_file = io.BytesIO(csv_content.encode())

    result = service.import_students_from_csv("course_id", csv_file)

    assert result.students_created == 1
    assert result.enrollments_created == 1
    assert result.rows_skipped == 1

    assert student_repo.get_by_email("jane@example.com") is not None
    assert student_repo.get_by_email("john.doe@example.com") is None


def test_import_raises_if_course_does_not_exist(enrollment_context):
    service = enrollment_context["service"]

    csv_content = """Vorname,Nachname,E-Mail-Adresse
John,Doe,john.doe@example.com
"""
    csv_file = io.BytesIO(csv_content.encode())

    with pytest.raises(CourseDoesNotExistException):
        service.import_students_from_csv("invalid_course_id", csv_file)


def test_import_raises_when_required_columns_missing(enrollment_context):
    service = enrollment_context["service"]

    csv_content = """Vorname,Nachname
John,Doe
"""
    csv_file = io.BytesIO(csv_content.encode())

    with pytest.raises(InvalidCsvFormat):
        service.import_students_from_csv("course_id", csv_file)


def test_multiple_students_are_imported(enrollment_context):
    service = enrollment_context["service"]
    student_repo = enrollment_context["student_repo"]

    csv_content = """Vorname,Nachname,E-Mail-Adresse
John,Doe,john@example.com
Jane,Doe,jane@example.com
"""
    csv_file = io.BytesIO(csv_content.encode())

    result = service.import_students_from_csv("course_id", csv_file)

    assert result.students_created == 2
    assert result.enrollments_created == 2
    assert result.rows_skipped == 0

    assert student_repo.get_by_email("john@example.com")
    assert student_repo.get_by_email("jane@example.com")


def test_mixed_valid_and_invalid_rows(enrollment_context):
    service = enrollment_context["service"]

    csv_content = """Vorname,Nachname,E-Mail-Adresse
John,Doe,
Jane,Doe,jane@example.com
Bob,Smith,
"""
    csv_file = io.BytesIO(csv_content.encode())

    result = service.import_students_from_csv("course_id", csv_file)

    assert result.students_created == 1
    assert result.enrollments_created == 1
    assert result.rows_skipped == 2


def test_on_moodle_csv(enrollment_context):
    service = enrollment_context["service"]

    csv_content = """Vorname,Nachname,E-Mail-Adresse,Gruppen
John,Doe,john@study.hs-duesseldorf.de,"Gruppe A"
Jane,Doe,jane@study.hs-duesseldorf.de,"Gruppe B (Programmierwoche B)"
Max,Doe,max@study.hs-duesseldorf.de,
"""
    csv_file = io.BytesIO(csv_content.encode())

    result = service.import_students_from_csv("course_id", csv_file)

    assert result.students_created == 3
    assert result.enrollments_created == 3
    assert result.rows_skipped == 0
