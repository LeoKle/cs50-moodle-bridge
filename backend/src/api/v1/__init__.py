from fastapi import APIRouter

from .controllers import course

router = APIRouter(prefix="/v1")

router.include_router(course.router)
