import json
from copy import deepcopy
from typing import BinaryIO

from exceptions.exceptions import InvalidJsonFormat
from interfaces.services.cs50_submission_problem_service import (
    ICS50SubmissionProblemService,
    SubmissionUploadResult,
)


class MockCS50SubmissionProblemService(ICS50SubmissionProblemService):
    def __init__(self):
        self._problems: dict[str, dict] = {}

    def seed(self, slug: str, submissions: list[dict]):
        self._problems[slug] = {
            "slug": slug,
            "submissions": deepcopy(submissions),
        }

    def get_submissions(self, slug: str):
        problem = self._problems.get(slug)
        if problem is None:
            return None
        return deepcopy(problem)

    def import_submissions_from_json(self, slug: str, file: BinaryIO) -> SubmissionUploadResult:
        try:
            payload = json.load(file)
        except Exception as exc:
            raise InvalidJsonFormat() from exc

        if slug not in payload:
            msg = f"Slug {slug} not found in JSON payload"
            raise ValueError(msg)

        submissions = payload.get(slug) or []
        if not isinstance(submissions, list):
            raise InvalidJsonFormat()

        self._problems[slug] = {"slug": slug, "submissions": deepcopy(submissions)}
        return SubmissionUploadResult(submissions_added=len(submissions))
