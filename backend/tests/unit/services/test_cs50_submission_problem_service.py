import io
import json

import pytest

from exceptions.exceptions import InvalidJsonFormat
from services.cs50_submission_problem import CS50SubmissionProblemService
from tests.mocks.repositories.cs50_submission_problem_repository_mock import (
    MockCS50SubmissionProblemRepository,
)

pytestmark = pytest.mark.unit


def make_file(payload) -> io.BytesIO:
    return io.BytesIO(json.dumps(payload).encode("utf-8"))


@pytest.fixture
def repo():
    return MockCS50SubmissionProblemRepository()


@pytest.fixture
def service(repo):
    return CS50SubmissionProblemService(repo)


def test_import_returns_0_when_slug_not_in_dict(service, repo):
    f = make_file({"other/slug": []})
    result = service.import_submissions_from_json("wanted/slug", f)

    assert result.submissions_added == 0
    assert repo.get_submissions("wanted/slug") is None


def test_import_dict_shape_saves_submissions(service, repo):
    slug = "hsddigitallabor/problems/adg2025/intervals"
    payload = {
        slug: [
            {
                "archive": "https://github.com/me50/github_name/archive/hash_value.zip",
                "checks_passed": 13,
                "checks_run": 13,
                "github_id": 123456789,
                "github_url": "https://github.com/me50/github_name/tree/hash_value",
                "github_username": "octocat",
                "name": None,
                "slug": slug,
                "style50_score": 1.0,
                "timestamp": "Mon, 01 Dec 2025 08:53:16PM CET",
            }
        ]
    }

    result = service.import_submissions_from_json(slug, make_file(payload))

    assert result.submissions_added == 1

    stored = repo.get_submissions(slug)
    assert stored is not None
    assert stored.slug == slug
    assert len(stored.submissions) == 1
    assert stored.submissions[0].github_username == "octocat"
    assert stored.submissions[0].name is None


def test_import_list_shape_saves_submissions(service, repo):
    slug = "some/slug"
    payload = [
        {
            "archive": "a",
            "checks_passed": 1,
            "checks_run": 1,
            "github_id": 1,
            "github_url": "u",
            "github_username": "user",
            "name": "Full Name",
            "slug": slug,
            "style50_score": 1.0,
            "timestamp": "Mon, 01 Dec 2025 08:53:16PM CET",
        }
    ]

    result = service.import_submissions_from_json(slug, make_file(payload))

    assert result.submissions_added == 1

    stored = repo.get_submissions(slug)
    assert stored is not None
    assert stored.submissions[0].name == "Full Name"


def test_import_raises_invalidjsonformat_for_wrong_top_level_type(service):
    f = make_file("not a dict or list")
    with pytest.raises(InvalidJsonFormat):
        service.import_submissions_from_json("any/slug", f)


def test_import_raises_invalidjsonformat_when_dict_value_is_not_list(service):
    f = make_file({"my/slug": {"not": "a list"}})
    with pytest.raises(InvalidJsonFormat):
        service.import_submissions_from_json("my/slug", f)


def test_import_raises_invalidjsonformat_for_invalid_json_text(service):
    f = io.BytesIO(b"{ this is not valid json")
    with pytest.raises(InvalidJsonFormat):
        service.import_submissions_from_json("any/slug", f)
