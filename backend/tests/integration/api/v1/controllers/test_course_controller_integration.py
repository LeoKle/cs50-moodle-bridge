import pytest
from fastapi import status

from api.models.course import CourseCreate, CourseOut, CourseUpdate

pytestmark = pytest.mark.integration


def test_get_course_success(client_course):
    response = client_course.get("/api/v1/courses/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_courses(client_course):
    response = client_course.get("/api/v1/courses")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_create_course_success(client_course):
    payload = CourseCreate(name="New Course", cs50_id=60, exercise_ids=[])

    response = client_course.post("/api/v1/courses", json=payload.model_dump())
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    model = CourseOut(**data)
    assert model.name == payload.name
    assert model.cs50_id == payload.cs50_id
    assert model.exercise_ids == payload.exercise_ids
    assert model.id != ""  # ensure ID is generated


def test_create_course_missing_fields(client_course):
    payload = {}
    response = client_course.post("/api/v1/courses", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_course_success(client_course):
    payload = CourseCreate(name="New Course", cs50_id=60, exercise_ids=[])

    response = client_course.post("/api/v1/courses", json=payload.model_dump())
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    created = CourseOut(**data)

    payload = CourseUpdate(name="Updated Name")

    response = client_course.patch(f"/api/v1/courses/{created.id}", json=payload.model_dump())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    model = CourseOut(**data)
    assert model.name == payload.name


def test_update_course_partial_update(client_course):
    payload = CourseCreate(name="New Course", cs50_id=60, exercise_ids=[])

    response = client_course.post("/api/v1/courses", json=payload.model_dump())
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    created = CourseOut(**data)

    payload = CourseUpdate(exercise_ids=["ex1", "ex2"])
    response = client_course.patch(f"/api/v1/courses/{created.id}", json=payload.model_dump())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    updated = CourseOut(**data)
    assert updated.id == created.id
    assert updated.exercise_ids == payload.exercise_ids


def test_update_course_not_found(client_course):
    payload = CourseUpdate(name="Does Not Exist")
    response = client_course.patch("/api/v1/courses/nonexistent", json=payload.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_delete_course_success(client_course):
    payload = CourseCreate(name="New Course", cs50_id=60, exercise_ids=[])

    response = client_course.post("/api/v1/courses", json=payload.model_dump())
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    created = CourseOut(**data)

    response = client_course.delete(f"/api/v1/courses/{created.id}")
    assert response.status_code == status.HTTP_200_OK

    response = client_course.get("/api/v1/courses/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_course_not_found(client_course):
    response = client_course.delete("/api/v1/courses/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_create_and_delete_multiple_courses(client_course):
    course_ids = []
    for i in range(3):
        payload = CourseCreate(name=f"Course {i}", cs50_id=i, exercise_ids=[])
        response = client_course.post("/api/v1/courses", json=payload.model_dump())
        assert response.status_code == status.HTTP_200_OK
        course_ids.append(response.json()["id"])

    # verify all exist
    response = client_course.get("/api/v1/courses")
    data = response.json()
    existing_ids = {c["id"] for c in data}
    for cid in course_ids:
        assert cid in existing_ids

    # delete all
    for cid in course_ids:
        response = client_course.delete(f"/api/v1/courses/{cid}")
        assert response.status_code == status.HTTP_200_OK

    # verify delete
    response = client_course.get("/api/v1/courses")
    data = response.json()
    remaining_ids = {c["id"] for c in data}
    for cid in course_ids:
        assert cid not in remaining_ids
