from uuid import uuid4

from pydantic import BaseModel, Field

from models.submission import SubmissionModel


class SubmissionProblemModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    slug: str
    submissions: list[SubmissionModel]
