from interfaces.repositories.cs50_submission_problem_repository_interface import (
    ICS50SubmissionProblemRepository,
)
from models.cs50_submission_problem import CS50SubmissionProblemModel
from models.submission import SubmissionModel


class MockCS50SubmissionProblemRepository(ICS50SubmissionProblemRepository):
    def __init__(self):
        self._data: dict[str, CS50SubmissionProblemModel] = {}

    def upload_submissions(self, slug: str, submissions: list[SubmissionModel]) -> None:
        self._data[slug] = CS50SubmissionProblemModel(slug=slug, submissions=submissions)

    def get_submissions(self, slug: str) -> CS50SubmissionProblemModel | None:
        return self._data.get(slug)
