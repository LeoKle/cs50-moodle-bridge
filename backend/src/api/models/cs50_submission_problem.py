from pydantic import BaseModel, ConfigDict, Field

from models.submission import SubmissionModel


class CS50SubmissionProblemCreate(BaseModel):
    slug: str = Field(..., min_length=1, description="CS50 problem slug (unique key)")


class CS50SubmissionsUploadIn(BaseModel):
    slug: str = Field(..., min_length=1, description="CS50 problem slug")
    submissions: list[SubmissionModel] = Field(default_factory=list)


class CS50SubmissionsUploadResult(BaseModel):
    slug: str
    uploaded: int = Field(..., ge=0, description="How many submissions were uploaded")


class CS50SubmissionProblemOut(BaseModel):
    id: str = Field(..., description="MongoDB ObjectId")
    slug: str
    submissions: list[SubmissionModel] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)
