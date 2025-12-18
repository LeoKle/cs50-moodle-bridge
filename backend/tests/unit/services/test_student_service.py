import pytest

from exceptions.duplicate_email import StudentEmailAlreadyExists
from models.student import StudentModel
from services.student import StudentService
from tests.mocks.repositories.student_repository_mock import MockStudentRepository

pytestmark = pytest.mark.unit


@pytest.fixture
def student_service():
    mock_repo = MockStudentRepository()
    return StudentService(mock_repo)


def test_create_student(student_service):
    student = StudentModel(email="first.last@email.com")

    created = student_service.create_student(student)

    assert student.id == created.id
    assert student.email == created.email


def test_create_duplicate_student(student_service):
    s1 = StudentModel(email="first.last@email.com")
    s2 = StudentModel(email="first.last@email.com")

    student_service.create_student(s1)

    with pytest.raises(StudentEmailAlreadyExists):
        student_service.create_student(s2)


def test_get_student(student_service):
    student = StudentModel(email="first.last@email.com")

    student_service.create_student(student)

    fetched = student_service.get_student(student.id)

    assert student.id == fetched.id
    assert student.email == fetched.email


def test_get_student_not_found(student_service):
    fetched = student_service.get_student("non_existent_id")

    assert fetched is None


def test_get_student_by_email_not_found(student_service):
    fetched = student_service.get_student_by_email("non.existent@email.com")

    assert fetched is None


def test_get_student_by_email(student_service):
    student = StudentModel(email="first.last@email.com")

    student_service.create_student(student)

    fetched = student_service.get_student_by_email(student.email)

    assert student.id == fetched.id
    assert student.email == fetched.email


def test_get_all_students(student_service):
    s1 = StudentModel(email="first.last@email.com")
    s2 = StudentModel(email="second.last@email.com")

    student_service.create_student(s1)
    student_service.create_student(s2)

    students = student_service.get_students()

    assert len(students) == 2
    ids = {s.id for s in students}
    assert s1.id in ids
    assert s2.id in ids


def test_update_student(student_service):
    student = StudentModel(email="first.last@email.com")
    student_service.create_student(student)

    update = StudentModel(
        id=student.id,
        email=student.email,
        name="Updated name",
        github_id=None,
        github_username="gh_username",
    )

    result = student_service.update_student(student.id, update)

    assert result is not None
    assert result.id == student.id
    assert result.name == update.name
    assert result.github_id == update.github_id


def test_delete_student(student_service):
    student = StudentModel(email="first.last@email.com")
    student_service.create_student(student)

    deleted = student_service.delete_student(student.id)

    assert deleted is True
    assert student_service.get_student(student.id) is None


def test_delete_non_existing_student(student_service):
    deleted = student_service.delete_student("non_existing")

    assert deleted is False
