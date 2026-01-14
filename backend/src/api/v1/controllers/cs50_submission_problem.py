from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from dependencies import DependencyContainer
from exceptions.exceptions import InvalidJsonFormat
from interfaces.services.cs50_submission_problem_service import ICS50SubmissionProblemService

router = APIRouter(prefix="/cs50/submissions", tags=["cs50"])


@router.post("/{slug:path}/import")
@inject
def import_submissions_from_json(
    slug: str,
    file: UploadFile,
    cs50_service: Annotated[
        ICS50SubmissionProblemService,
        Depends(Provide(DependencyContainer.cs50_submission_problem_service)),
    ],
):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JSON file required.",
        )

    allowed = {"application/json", "text/json", "application/octet-stream"}
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. JSON required.",
        )

    try:
        result = cs50_service.import_submissions_from_json(slug=slug, file=file.file)
    except InvalidJsonFormat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format.",
        ) from None
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from None

    return {"slug": slug, "submissions_added": result.submissions_added}


@router.get("/{slug:path}")
@inject
def get_submissions(
    slug: str,
    cs50_service: Annotated[
        ICS50SubmissionProblemService,
        Depends(Provide(DependencyContainer.cs50_submission_problem_service)),
    ],
):
    result = cs50_service.get_submissions(slug)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CS50 submissions with slug {slug} not found",
        )

    return result
