from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import BinaryIO


@dataclass(frozen=True)
class SubmissionUploadResult:
    submissions_added: int


class ISubmissionProblemService(ABC):
    @abstractmethod
    def import_submissions_from_json(
        self, slug: str, file: BinaryIO
    ) -> SubmissionUploadResult: ...
