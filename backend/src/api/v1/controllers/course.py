from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from api.models.course import CourseCreate, CourseOut, CourseUpdate
from dependencies import DependencyContainer
from interfaces.services.course_service import ICourseService
from models.course import Course

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/{course_id}", response_model=CourseOut)
@inject
def get_course(
    course_id: str,
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    result: Course = course_service.get_course(course_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {course_id} not found"
        )

    return CourseOut(**result.model_dump())


@router.get("", response_model=list[CourseOut])
@inject
def get_courses(
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    results = course_service.get_courses()
    return [CourseOut(**course.model_dump()) for course in results]


@router.post("", response_model=CourseOut)
@inject
def create_course(
    data: CourseCreate,
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    course = Course(
        name=data.name,
        cs50_id=data.cs50_id,
        exercise_ids=list(data.exercise_ids) if data.exercise_ids else [],
    )
    created_course = course_service.create_course(course)
    return CourseOut(**created_course.model_dump())


@router.patch("/{course_id}", response_model=CourseOut)
@inject
def update_course(
    course_id: str,
    data: CourseUpdate,
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    # get existing course
    existing_course = course_service.get_course(course_id)
    if not existing_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {course_id} not found"
        )
    # merge fields
    updated_data = data.model_dump(exclude_unset=True, exclude_defaults=True)
    updated_course = Course(
        id=existing_course.id,
        name=updated_data.get("name", existing_course.name),
        cs50_id=updated_data.get("cs50_id", existing_course.cs50_id),
        exercise_ids=updated_data.get("exercise_ids", existing_course.exercise_ids),
    )

    saved_course = course_service.update_course(course_id, updated_course)
    return CourseOut(**saved_course.model_dump())


@router.delete("/{course_id}")
@inject
def delete_course(
    course_id: str,
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    deleted = course_service.delete_course(course_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {course_id} not found"
        )
    return
