from uuid import uuid4

from pydantic import BaseModel, Field


class StudentModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    email: str
    github_id: int | None = None
    name: str = ""
    github_username: str = ""
