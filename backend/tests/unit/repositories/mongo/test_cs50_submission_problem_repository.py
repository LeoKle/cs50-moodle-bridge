import json
from pathlib import Path

import mongomock
import pytest

from models.cs50_submission_problem import CS50SubmissionProblemModel
from models.submission import SubmissionModel
from repositories.mongo.cs50_submission_problem_repository import MongoSubmissionProblemRepository
from repositories.mongo.migration import init_cs50_submission_problem_collection

pytestmark = pytest.mark.unit


@pytest.fixture()
def collection():
    client = mongomock.MongoClient()
    db = client["test-db"]
    col = db["cs50_submissions"]
    init_cs50_submission_problem_collection(col)
    return col


@pytest.fixture()
def repo(collection):
    return MongoSubmissionProblemRepository(collection)


def test_get_submissions_returns_none_if_not_found(repo):
    assert repo.get_submissions("does/not/exist") is None


def test_upload_and_get_submissions_roundtrip(repo):
    slug = "hsddigitallabor/problems/adg2025/intervals"

    submissions = [
        SubmissionModel.model_validate({
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
        })
    ]

    model = CS50SubmissionProblemModel(slug=slug, submissions=submissions)

    repo.upload_submissions(model)

    loaded = repo.get_submissions(slug)
    assert loaded is not None
    assert loaded.slug == slug
    assert len(loaded.submissions) == 1
    assert loaded.submissions[0].github_username == "octocat"
    assert loaded.submissions[0].name is None


def test_upload_submissions_updates_existing_slug(repo):
    slug = "same/slug"

    first = CS50SubmissionProblemModel(
        slug=slug,
        submissions=[
            SubmissionModel.model_validate({
                "archive": "a",
                "checks_passed": 1,
                "checks_run": 1,
                "github_id": 1,
                "github_url": "u1",
                "github_username": "user1",
                "name": None,
                "slug": slug,
                "style50_score": 1.0,
                "timestamp": "Mon, 01 Dec 2025 08:53:16PM CET",
            })
        ],
    )

    second = CS50SubmissionProblemModel(
        slug=slug,
        submissions=[
            SubmissionModel.model_validate({
                "archive": "b",
                "checks_passed": 2,
                "checks_run": 2,
                "github_id": 2,
                "github_url": "u2",
                "github_username": "user2",
                "name": "Full Name",
                "slug": slug,
                "style50_score": 1.0,
                "timestamp": "Mon, 01 Dec 2025 08:20:07PM CET",
            })
        ],
    )

    repo.upload_submissions(first)
    repo.upload_submissions(second)

    loaded = repo.get_submissions(slug)
    assert loaded is not None
    assert len(loaded.submissions) == 1
    assert loaded.submissions[0].archive == "b"
    assert loaded.submissions[0].github_username == "user2"


def test_upload_and_get_with_sample_cs50_json(repo):

    PROJECT_ROOT = Path(__file__).resolve().parents[5]
    DATA_FILE = PROJECT_ROOT / "data" / "cs50.json"

    with Path(DATA_FILE).open(encoding="utf-8") as f:
        data = json.load(f)

    slug = next(iter(data.keys()))
    items = data[slug]

    submissions = [SubmissionModel.model_validate(item) for item in items]

    model = CS50SubmissionProblemModel(slug=slug, submissions=submissions)
    repo.upload_submissions(model)

    loaded = repo.get_submissions(slug)
    assert loaded is not None
    assert loaded.slug == slug
    assert len(loaded.submissions) == len(items)
