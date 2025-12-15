import pytest

from api.models.course import CourseCreate, CourseOut, CourseUpdate

pytestmark = pytest.mark.unit


def test_get_course(client):
    response = client.get("/api/v1/courses/1")
    assert response.status_code == 200

    data = response.json()
    model = CourseOut(**data)
    assert model.id == "1"


def test_get_courses(client):
    response = client.get("/api/v1/courses")
    assert response.status_code == 200

    data = response.json()
    for element in data:
        CourseOut(**element)


def test_create_course(client):
    payload = CourseCreate(name="New Course", cs50_id=60, exercise_ids=[])

    response = client.post("/api/v1/courses", json=payload.model_dump())
    assert response.status_code == 200

    data = response.json()
    model = CourseOut(**data)
    assert model.name == payload.name
    assert model.cs50_id == payload.cs50_id
    assert model.exercise_ids == payload.exercise_ids
    assert model.id != ""  # ensure ID is generated


def test_update_course(client):
    payload = CourseUpdate(name="Updated Name")

    response = client.patch("/api/v1/courses/1", json=payload.model_dump())
    assert response.status_code == 200
    data = response.json()
    model = CourseOut(**data)
    assert model.name == payload.name


def test_delete_course(client):
    response = client.delete("/api/v1/courses/1")
    assert response.status_code == 200

    courses = client.get("/api/v1/courses")
    courses = courses.json()
    ids = {c["id"] for c in courses}
    assert "1" not in ids
