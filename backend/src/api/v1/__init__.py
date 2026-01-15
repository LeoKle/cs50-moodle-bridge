from fastapi import APIRouter

from .controllers import course, cs50_submission_problem, enrollment

router = APIRouter(prefix="/v1")

router.include_router(course.router)
router.include_router(enrollment.router)
router.include_router(cs50_submission_problem.router)
