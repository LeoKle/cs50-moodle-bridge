from abc import ABC, abstractmethod

from models.submission import SubmissionModel
from models.submission_problem import SubmissionProblemModel


class ISubmissionProblemRepository(ABC):
    @abstractmethod
    def upload_submissions(self, slug: str, submissions: list[SubmissionModel]) -> None: ...

    @abstractmethod
    def get_submissions(self, slug: str) -> SubmissionProblemModel | None: ...
