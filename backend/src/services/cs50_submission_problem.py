import json
from typing import BinaryIO

from exceptions.exceptions import InvalidJsonFormat
from interfaces.repositories.cs50_submission_problem_repository_interface import (
    ICS50SubmissionProblemRepository,
)
from interfaces.services.cs50_submission_problem_service import (
    ICS50SubmissionProblemService,
    SubmissionUploadResult,
)
from models.submission import SubmissionModel


class CS50SubmissionProblemService(ICS50SubmissionProblemService):
    def __init__(self, repo: ICS50SubmissionProblemRepository):
        self._repo = repo

    def import_submissions_from_json(self, slug: str, file: BinaryIO) -> SubmissionUploadResult:
        raw = file.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise InvalidJsonFormat from exc

        if isinstance(data, dict):
            if slug not in data:
                return SubmissionUploadResult(submissions_added=0)
            submission_items = data[slug]
        elif isinstance(data, list):
            submission_items = data
        else:
            raise InvalidJsonFormat

        if not isinstance(submission_items, list):
            raise InvalidJsonFormat

        submissions: list[SubmissionModel] = [
            SubmissionModel.model_validate(item) for item in submission_items
        ]

        self._repo.upload_submissions(slug, submissions)

        return SubmissionUploadResult(submissions_added=len(submissions))
