"""Pydantic models for course data structures."""

from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    """Data required to create a new course."""

    name: str = Field(..., min_length=1, description="Course name")
    cs50_id: int | None = Field(default=None, description="CS50 course identifier")
    exercise_ids: list[str] | None = Field(
        default=None, description="List of exercise document IDs"
    )


class CourseUpdate(BaseModel):
    """Data to update an existing course; all fields optional."""

    name: str | None = Field(None, min_length=1, description="Course name")
    cs50_id: int | None = Field(default=None, description="CS50 course identifier")
    exercise_ids: list[str] | None = Field(
        default=None, description="List of exercise document IDs"
    )


class CourseOut(BaseModel):
    """Data returned to the client."""

    id: str = Field(
        ...,
        alias="_id",
        validation_alias=AliasChoices("_id", "id"),
        description="MongoDB ObjectId",
    )
    name: str
    cs50_id: int | None = None
    exercise_ids: list[str] = []

    model_config = ConfigDict(populate_by_name=True)

    def __getitem__(self, item: str) -> Any:
        return self.model_dump().get(item)

    def __contains__(self, item: object) -> bool:
        return bool(isinstance(item, str) and item in self.model_dump())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CourseOut):
            return super().__eq__(other)
        if isinstance(other, dict):
            return self.model_dump() == other
        return False
