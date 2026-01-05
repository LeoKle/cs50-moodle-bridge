import enum
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


class GradeType(enum.StrEnum):
    pass_fail = "pass_fail"
    numeric = "numeric"


class PassFailGrade(int, enum.Enum):
    failed = 0
    passed = 1


class MoodleWorksheetRowModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    submission_id: str
    email: str
    status: str

    grade_type: GradeType

    grade_numeric: float | None = None
    grade_pass_fail: PassFailGrade | None = None
    grade_scale: str
    grade_can_be_changed: bool = True
    submission_last_modified: datetime
    grade_last_modified: datetime
    feedback_comment: str

    # optional fields:
    submission_begin: datetime | None = None
    deadline: datetime | None = None
    last_submission: datetime | None = None

    @model_validator(mode="after")
    def validate_grade(self):
        if self.grade_type == GradeType.numeric and (
            self.grade_numeric is None or self.grade_pass_fail is not None
        ):
            msg = "Numeric grade requires grade_numeric only"
            raise ValueError(msg)

        if self.grade_type == GradeType.pass_fail and (
            self.grade_pass_fail is None or self.grade_numeric is not None
        ):
            msg = "Pass/fail grade requires grade_pass_fail only"
            raise ValueError(msg)

        return self
