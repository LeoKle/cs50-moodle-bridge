from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    """Data required to create a new course."""

    name: str = Field(..., min_length=1, description="Course name")
    cs50_id: int | None = Field(default=None, description="CS50 course identifier")
    exercise_ids: list[str] | None = Field(
        default_factory=list, description="List of exercise document IDs"
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

    id: str = Field(..., description="MongoDB ObjectId")
    name: str
    cs50_id: int | None = None
    exercise_ids: list[str] = []

    model_config = ConfigDict(populate_by_name=True)  # Allows using both id and _id
