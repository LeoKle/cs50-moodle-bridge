"""Domain models for data validation and type safety."""

from typing import Any, ClassVar

from pydantic import BaseModel, Field


class Course(BaseModel):
    """Course domain model.

    Represents a course with exercises stored as references to a separate collection.
    """

    id: str | None = Field(default=None, alias="_id", description="MongoDB ObjectId")
    name: str = Field(..., min_length=1, description="Course name")
    cs50_id: int = Field(..., description="CS50 course identifier")
    exercise_ids: list[str] = Field(
        default_factory=list, description="List of exercise document IDs"
    )

    class Config:
        """Pydantic model configuration."""

        populate_by_name = True  # Allow both 'id' and '_id'
        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "Introduction to Computer Science",
                "cs50_id": 50,
                "exercise_ids": [
                    "507f191e810c19729de860ea",
                    "507f191e810c19729de860eb",
                ],
            }
        }
