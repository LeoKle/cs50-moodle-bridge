from abc import ABC, abstractmethod

from models.cs50_submission_problem import CS50SubmissionProblemModel
from models.submission import SubmissionModel


class ICS50SubmissionProblemRepository(ABC):
    @abstractmethod
    def upload_submissions(self, slug: str, submissions: list[SubmissionModel]) -> None: ...

    @abstractmethod
    def get_submissions(self, slug: str) -> CS50SubmissionProblemModel | None: ...
