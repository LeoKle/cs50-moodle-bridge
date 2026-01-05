from datetime import datetime

from dateutil import parser
from pydantic import BaseModel, field_validator


class SubmissionModel(BaseModel):
    archive: str
    checks_passed: int | None
    checks_run: int | None
    github_id: int
    github_url: str
    github_username: str
    name: str | None
    slug: str
    timestamp: datetime

    @field_validator("timestamp", mode="before")
    def parse_timestamp(cls, v):
        dt = parser.parse(v)
        return dt
