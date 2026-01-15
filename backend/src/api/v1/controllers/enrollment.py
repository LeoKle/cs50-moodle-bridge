from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from dependencies import DependencyContainer
from exceptions.exceptions import CourseDoesNotExistException
from interfaces.services.enrollment_service import IEnrollmentService

router = APIRouter(prefix="/enroll", tags=["enrollment"])


@router.post("/{course_id}")
@inject
def import_students_from_csv(
    course_id: str,
    file: UploadFile,
    enrollment_service: Annotated[
        IEnrollmentService, Depends(Provide(DependencyContainer.enrollment_service))
    ],
):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV required.",
        )

    if file.content_type not in {"text/csv", "application/vnd.ms-excel"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. CSV required.",
        )

    try:
        result = enrollment_service.import_students_from_csv(
            course_id=course_id,
            file=file.file,
        )
    except CourseDoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course does not exist",
        ) from None
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from None
    else:
        return result
