from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import BinaryIO


@dataclass(frozen=True)
class EnrollmentImportResult:
    students_created: int
    enrollments_created: int
    rows_skipped: int


class IEnrollmentService(ABC):
    @abstractmethod
    def import_students_from_csv(
        self, course_id: str, file: BinaryIO
    ) -> EnrollmentImportResult: ...
