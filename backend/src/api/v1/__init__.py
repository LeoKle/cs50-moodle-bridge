from fastapi import APIRouter

from .controllers import course, enrollment

router = APIRouter(prefix="/v1")

router.include_router(course.router)
router.include_router(enrollment.router)
