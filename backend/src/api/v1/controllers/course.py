from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from api.models.course import CourseCreate, CourseOut, CourseUpdate
from dependencies import DependencyContainer
from interfaces.services.course_service import ICourseService

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/{course_id}", response_model=CourseOut)
@inject
def get_course(
    course_id: str,
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    return course_service.get_course(course_id)


@router.get("", response_model=list[CourseOut])
@inject
def get_courses(
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    return course_service.get_courses()


@router.post("", response_model=CourseOut)
@inject
def create_course(
    data: CourseCreate,
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    return course_service.create_course(data)


@router.patch("/{course_id}", response_model=CourseOut)
@inject
def update_course(
    course_id: str,
    data: CourseUpdate,
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    return course_service.update_course(course_id, data)


@router.delete("/{course_id}")
@inject
def delete_course(
    course_id: str,
    course_service: Annotated[ICourseService, Depends(Provide(DependencyContainer.course_service))],
):
    course_service.delete_course(course_id)
