from pydantic import BaseModel


class Course(BaseModel):
    id: str
    name: str
    cs50_id: int | None = None
    exercise_ids: list[str] = []
