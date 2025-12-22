import pytest

from models.enrollment import EnrollmentModel

pytestmark = pytest.mark.unit


def test_add_enrollment(enrollment_repository):
    enrollment = EnrollmentModel(
        student_id="student_1",
        course_id="course_1",
    )

    enrollment_repository.add_enrollment(enrollment)

    courses = enrollment_repository.get_courses_for_student("student_1")

    assert courses == ["course_1"]


def test_get_courses_for_student_multiple(enrollment_repository):
    enrollments = [
        EnrollmentModel(student_id="student_1", course_id="course_1"),
        EnrollmentModel(student_id="student_1", course_id="course_2"),
        EnrollmentModel(student_id="student_2", course_id="course_3"),
    ]

    for enrollment in enrollments:
        enrollment_repository.add_enrollment(enrollment)

    courses = enrollment_repository.get_courses_for_student("student_1")

    assert set(courses) == {"course_1", "course_2"}


def test_get_students_for_course(enrollment_repository):
    enrollments = [
        EnrollmentModel(student_id="student_1", course_id="course_1"),
        EnrollmentModel(student_id="student_2", course_id="course_1"),
        EnrollmentModel(student_id="student_3", course_id="course_2"),
    ]

    for enrollment in enrollments:
        enrollment_repository.add_enrollment(enrollment)

    students = enrollment_repository.get_students_for_course("course_1")

    assert set(students) == {"student_1", "student_2"}


def test_remove_enrollment_success(enrollment_repository):
    enrollment = EnrollmentModel(
        student_id="student_1",
        course_id="course_1",
    )

    enrollment_repository.add_enrollment(enrollment)

    removed = enrollment_repository.remove_enrollment(enrollment)

    assert removed is True
    assert enrollment_repository.get_courses_for_student("student_1") == []


def test_remove_enrollment_not_found(enrollment_repository):
    enrollment = EnrollmentModel(
        student_id="student_1",
        course_id="course_1",
    )

    removed = enrollment_repository.remove_enrollment(enrollment)

    assert removed is False


def test_add_bulk_enrollments(enrollment_repository):
    enrollments = [
        EnrollmentModel(student_id="student_1", course_id="course_1"),
        EnrollmentModel(student_id="student_1", course_id="course_2"),
        EnrollmentModel(student_id="student_2", course_id="course_1"),
    ]

    enrollment_repository.add_bulk_enrollments(enrollments)

    assert set(enrollment_repository.get_courses_for_student("student_1")) == {
        "course_1",
        "course_2",
    }

    assert set(enrollment_repository.get_students_for_course("course_1")) == {
        "student_1",
        "student_2",
    }


def test_add_bulk_enrollments_empty_list(enrollment_repository):
    enrollment_repository.add_bulk_enrollments([])

    assert enrollment_repository.get_courses_for_student("student_1") == []
