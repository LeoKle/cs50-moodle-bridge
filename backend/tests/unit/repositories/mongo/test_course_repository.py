import pytest

from models.course import Course

pytestmark = pytest.mark.unit


def test_create_course(course_repository):
    course = Course(name="Course 1", cs50_id=50)

    created = course_repository.create(course)

    assert created.id == course.id
    assert created.name == "Course 1"


def test_get_course(course_repository):
    course = Course(name="Course 1", cs50_id=50)
    course_repository.create(course)

    fetched = course_repository.get(course.id)

    assert fetched is not None
    assert fetched.id == course.id
    assert fetched.name == course.name


def test_get_course_not_found(course_repository):
    fetched = course_repository.get("nonexistent")
    assert fetched is None


def test_get_all_courses(course_repository):
    c1 = Course(name="Course 1", cs50_id=50)
    c2 = Course(name="Course 2", cs50_id=60)

    course_repository.create(c1)
    course_repository.create(c2)

    courses = course_repository.get_all()

    assert len(courses) == 2
    ids = {c.id for c in courses}
    assert c1.id in ids
    assert c2.id in ids


def test_update_course(course_repository):
    course = Course(name="Course 1", cs50_id=50)
    course_repository.create(course)

    updated = Course(
        id=course.id,
        name="Updated Course",
        cs50_id=course.cs50_id,
        exercise_ids=course.exercise_ids,
    )

    result = course_repository.update(course.id, updated)

    assert result is not None
    assert result.name == "Updated Course"


def test_update_course_not_found(course_repository):
    course = Course(name="Course 1", cs50_id=50)

    result = course_repository.update("missing", course)

    assert result is None


def test_delete_course(course_repository):
    course = Course(name="Course 1")
    course_repository.create(course)

    deleted = course_repository.delete(course.id)

    assert deleted is True
    assert course_repository.get(course.id) is None


def test_delete_course_not_found(course_repository):
    deleted = course_repository.delete("missing")
    assert deleted is False
