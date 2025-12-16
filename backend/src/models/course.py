from uuid import uuid4

from pydantic import BaseModel, Field


class Course(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    cs50_id: int | None = None
    exercise_ids: list[str] = []
