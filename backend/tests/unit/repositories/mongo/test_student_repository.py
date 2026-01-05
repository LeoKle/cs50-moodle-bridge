import pytest

from exceptions.duplicate_email import StudentEmailAlreadyExists
from models.student import StudentModel

pytestmark = pytest.mark.unit


def test_create_student(student_repository):
    student = StudentModel(email="first.last@email.com")

    created = student_repository.create(student)

    assert student.id == created.id
    assert student.email == created.email


def test_create_duplicate_student(student_repository):
    s1 = StudentModel(email="first.last@email.com")
    s2 = StudentModel(email="first.last@email.com")

    student_repository.create(s1)

    with pytest.raises(StudentEmailAlreadyExists):
        student_repository.create(s2)


def test_get_student(student_repository):
    student = StudentModel(email="first.last@email.com")

    student_repository.create(student)

    fetched = student_repository.get(student.id)

    assert student.id == fetched.id
    assert student.email == fetched.email


def test_get_student_not_found(student_repository):
    fetched = student_repository.get("non_existent_id")

    assert fetched is None


def test_get_student_by_email_not_found(student_repository):
    fetched = student_repository.get_by_email("non.existent@email.com")

    assert fetched is None


def test_get_student_by_email(student_repository):
    student = StudentModel(email="first.last@email.com")

    student_repository.create(student)

    fetched = student_repository.get_by_email(student.email)

    assert student.id == fetched.id
    assert student.email == fetched.email


def test_get_all_students(student_repository):
    s1 = StudentModel(email="first.last@email.com")
    s2 = StudentModel(email="second.last@email.com")

    student_repository.create(s1)
    student_repository.create(s2)

    students = student_repository.get_all()

    assert len(students) == 2
    ids = {s.id for s in students}
    assert s1.id in ids
    assert s2.id in ids


def test_update_student(student_repository):
    student = StudentModel(email="first.last@email.com")
    student_repository.create(student)

    update = StudentModel(
        id=student.id,
        email=student.email,
        name="Updated name",
        github_id=None,
        github_username="gh_username",
    )

    result = student_repository.update(student.id, update)

    assert result is not None
    assert result.id == student.id
    assert result.name == update.name
    assert result.github_id == update.github_id


def test_delete_student(student_repository):
    student = StudentModel(email="first.last@email.com")
    student_repository.create(student)

    deleted = student_repository.delete(student.id)

    assert deleted is True
    assert student_repository.get(student.id) is None


def test_delete_non_existing_student(student_repository):
    deleted = student_repository.delete("non_existing")

    assert deleted is False
