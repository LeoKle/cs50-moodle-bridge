import io
import json

import pytest
from fastapi import status

pytestmark = pytest.mark.unit

# GET


def test_get_submissions_success(client, cs50_submission_problem_fixture):
    slug = "hsddigitallabor/problems/adg2025/intervals"

    response = client.get(f"/api/v1/cs50/submissions/{slug}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["slug"] == slug
    assert "submissions" in data
    assert isinstance(data["submissions"], list)


def test_get_submissions_not_found_returns_404(client):
    response = client.get("/api/v1/cs50/submissions/does/not/exist")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert "not found" in data["detail"].lower()


def test_get_submissions_border_empty_slug_path_returns_404(
    client, cs50_submission_problem_fixture
):
    response = client.get("/api/v1/cs50/submissions/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_submissions_success_returns_seeded_values(client, cs50_submission_problem_fixture):
    slug = "hsddigitallabor/problems/adg2025/intervals"

    response = client.get(f"/api/v1/cs50/submissions/{slug}")
    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["slug"] == slug
    assert "submissions" in body
    assert isinstance(body["submissions"], list)
    assert len(body["submissions"]) == 1

    submission = body["submissions"][0]

    assert submission["archive"] == "https://github.com/me50/test/archive/abc123.zip"
    assert submission["checks_passed"] == 13
    assert submission["checks_run"] == 13
    assert submission["github_id"] == 123
    assert submission["github_url"] == "https://github.com/me50/test/tree/abc123"
    assert submission["github_username"] == "testuser"
    assert submission["name"] == "Interval Assignment"
    assert submission["slug"] == slug

    assert isinstance(submission["timestamp"], str)
    assert submission["timestamp"].startswith("2025-12-01T20:53:16")


# POST


def test_import_submissions_success_application_json(client, cs50_submission_problem_fixture):
    slug = "hsddigitallabor/problems/adg2025/intervals"
    payload = {
        slug: [
            {"github_id": 1, "checks_run": 1, "checks_passed": 1},
            {"github_id": 2, "checks_run": 2, "checks_passed": 2},
        ]
    }
    file_bytes = json.dumps(payload).encode("utf-8")

    response = client.post(
        f"/api/v1/cs50/submissions/{slug}/import",
        files={"file": ("cs50.json", io.BytesIO(file_bytes), "application/json")},
    )
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["slug"] == slug
    assert data["submissions_added"] == 2

    get_response = client.get(f"/api/v1/cs50/submissions/{slug}")
    assert get_response.status_code == status.HTTP_200_OK
    get_data = get_response.json()
    assert len(get_data["submissions"]) == 2


def test_import_submissions_success_octet_stream_allowed(client, cs50_submission_problem_fixture):
    slug = "hsddigitallabor/problems/adg2025/intervals"
    payload = {slug: []}
    file_bytes = json.dumps(payload).encode("utf-8")

    response = client.post(
        f"/api/v1/cs50/submissions/{slug}/import",
        files={"file": ("cs50.json", io.BytesIO(file_bytes), "application/octet-stream")},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["submissions_added"] == 0


def test_import_submissions_invalid_content_type_returns_400(
    client, cs50_submission_problem_fixture
):
    slug = "hsddigitallabor/problems/adg2025/intervals"

    response = client.post(
        f"/api/v1/cs50/submissions/{slug}/import",
        files={"file": ("cs50.txt", io.BytesIO(b"{}"), "text/plain")},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "json required" in response.json()["detail"].lower()


def test_import_submissions_invalid_json_returns_400(client, cs50_submission_problem_fixture):
    slug = "hsddigitallabor/problems/adg2025/intervals"

    response = client.post(
        f"/api/v1/cs50/submissions/{slug}/import",
        files={"file": ("cs50.json", io.BytesIO(b"{not valid json"), "application/json")},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "invalid json format" in response.json()["detail"].lower()


def test_import_submissions_slug_missing_in_payload_returns_400(
    client, cs50_submission_problem_fixture
):
    slug = "hsddigitallabor/problems/adg2025/intervals"
    payload = {"some/other/slug": []}
    file_bytes = json.dumps(payload).encode("utf-8")

    response = client.post(
        f"/api/v1/cs50/submissions/{slug}/import",
        files={"file": ("cs50.json", io.BytesIO(file_bytes), "application/json")},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not found" in response.json()["detail"].lower()


def test_import_submissions_missing_file_returns_422(client, cs50_submission_problem_fixture):
    slug = "hsddigitallabor/problems/adg2025/intervals"

    response = client.post(f"/api/v1/cs50/submissions/{slug}/import")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_import_submissions_wrong_field_name_returns_422(client, cs50_submission_problem_fixture):
    slug = "hsddigitallabor/problems/adg2025/intervals"
    payload = {slug: []}
    file_bytes = json.dumps(payload).encode("utf-8")

    response = client.post(
        f"/api/v1/cs50/submissions/{slug}/import",
        files={"wrong_name": ("cs50.json", io.BytesIO(file_bytes), "application/json")},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_submissions_not_found_returns_404_2(client):
    """
    No seed for this slug -> service returns None -> controller should return 404.
    """
    slug = "does/not/exist"

    response = client.get(f"/api/v1/cs50/submissions/{slug}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
