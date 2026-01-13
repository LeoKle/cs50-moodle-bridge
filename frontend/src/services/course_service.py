import os

import requests
from interfaces.services import CourseServiceInterface
from models.course import CourseCreate, CourseOut
from pydantic import ValidationError


class CourseServiceError(Exception):
    """Custom exception for CourseService errors."""


class CourseService(CourseServiceInterface):
    """Service to handle course-related API calls to the backend."""

    def __init__(self) -> None:
        """Initialize the CourseService with backend URL configuration."""
        self.base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.api_url = f"{self.base_url}/api/v1/courses"

    def get_courses(self) -> list[CourseOut]:
        """Fetch all courses from the backend and validate with pydantic."""
        try:
            response = requests.get(self.api_url, timeout=30)
            response.raise_for_status()
            payload = response.json()
            return [CourseOut.model_validate(item) for item in payload]
        except (requests.exceptions.RequestException, ValidationError) as e:
            msg = f"Failed to fetch courses: {e!s}"
            raise CourseServiceError(msg) from e

    def get_course(self, course_id: str) -> CourseOut:
        """Fetch a single course by ID from the backend and validate response."""
        try:
            response = requests.get(f"{self.api_url}/{course_id}", timeout=30)
            response.raise_for_status()
            return CourseOut.model_validate(response.json())
        except (requests.exceptions.RequestException, ValidationError) as e:
            msg = f"Failed to fetch course: {e!s}"
            raise CourseServiceError(msg) from e

    def create_course(self, course: CourseCreate | str, cs50_id: int | None = None) -> CourseOut:
        """Create a new course using validated input and validate the response."""
        try:
            payload = (
                CourseCreate(name=course, cs50_id=cs50_id)
                if isinstance(course, str)
                else CourseCreate.model_validate(course)
            )
            response = requests.post(
                self.api_url,
                json=payload.model_dump(by_alias=True, exclude_none=True),
                timeout=30,
            )
            response.raise_for_status()
            return CourseOut.model_validate(response.json())
        except (requests.exceptions.RequestException, ValidationError) as e:
            msg = f"Failed to create course: {e!s}"
            raise CourseServiceError(msg) from e
