import pytest

from models.course import Course
from services.course import CourseService
from tests.mocks.repositories.course_repository_mock import MockCourseRepository

pytestmark = pytest.mark.unit


@pytest.fixture
def course_service():
    mock_repo = MockCourseRepository()
    return CourseService(mock_repo)


def test_get_course_returns_none_when_not_found(course_service):
    result = course_service.get_course("non_existent_id")
    assert result is None


def test_get_course_returns_course_when_found(course_service):
    course = Course(name="some course", cs50_id=50, exercise_ids=[])
    course_service.create_course(course.model_copy())

    result = course_service.get_course(course.id)

    assert result is not None
    assert result.id == course.id
    assert result.name == course.name


def test_get_courses_returns_empty_list_initially(course_service):
    courses = course_service.get_courses()
    assert courses == []


def test_get_courses_returns_all_created_courses(course_service):
    course1 = Course(id="1", name="course 1", cs50_id=10, exercise_ids=[])
    course2 = Course(id="2", name="course 2", cs50_id=20, exercise_ids=[])

    course_service.create_course(course1.model_copy())
    course_service.create_course(course2.model_copy())

    courses = course_service.get_courses()

    assert len(courses) == 2
    assert {c.id for c in courses} == {"1", "2"}


def test_create_course_does_not_mutate_input(course_service):
    course = Course(name="some course", cs50_id=50, exercise_ids=[])

    result = course_service.create_course(course.model_copy())

    # original object remains unchanged
    assert course == result


def test_create_course_persists_course(course_service):
    course = Course(name="some course", cs50_id=50, exercise_ids=[])

    created = course_service.create_course(course.model_copy())
    fetched = course_service.get_course(created.id)

    assert fetched is not None
    assert fetched.id == created.id


def test_update_course_updates_existing_course(course_service):
    original = Course(name="course", cs50_id=50, exercise_ids=[])
    created = course_service.create_course(original.model_copy())

    update_data = Course(id=created.id, name="updated course", cs50_id=99, exercise_ids=[])

    updated = course_service.update_course(created.id, update_data.model_copy())

    assert updated is not None
    assert updated.id == created.id
    assert updated.name == "updated course"
    assert updated.cs50_id == 99


def test_update_course_returns_none_when_course_does_not_exist(course_service):
    course = Course(name="course", cs50_id=50, exercise_ids=[])

    result = course_service.update_course(course.id, course.model_copy())

    assert result is None


def test_update_course_does_not_create_new_course(course_service):
    course = Course(name="course", cs50_id=50, exercise_ids=[])

    course_service.update_course(course.id, course.model_copy())

    assert course_service.get_courses() == []


def test_delete_course_removes_existing_course(course_service):
    course = Course(name="course", cs50_id=50, exercise_ids=[])
    created = course_service.create_course(course.model_copy())

    result = course_service.delete_course(created.id)

    assert result is True
    assert course_service.get_course(created.id) is None
    assert course_service.get_courses() == []


def test_delete_course_returns_false_when_course_does_not_exist(course_service):
    result = course_service.delete_course("missing")

    assert result is False
