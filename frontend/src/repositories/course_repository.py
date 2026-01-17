"""Course repository - handles HTTP communication with backend API."""

import httpx
from pydantic import ValidationError

import constants as const
from config.settings import get_api_settings
from interfaces.repositories.course_repository_interface import (
    CourseRepositoryInterface,
)
from models.course import CourseCreate, CourseOut, CourseUpdate


class CourseRepositoryError(Exception):
    """Custom exception for CourseRepository errors."""


class CourseRepository(CourseRepositoryInterface):
    """Production implementation - calls actual backend API."""

    def __init__(self):
        """Initialize repository with HTTP client."""
        self._settings = get_api_settings()
        self._client = httpx.Client(
            base_url=self._settings.backend_url, timeout=self._settings.timeout
        )
        self._api_path = f"{const.API_V1_PREFIX}{const.COURSES_ENDPOINT}"

    def get_all(self) -> list[CourseOut]:
        """Fetch all courses from backend API."""
        try:
            response = self._client.get(self._api_path)
            response.raise_for_status()
            return [CourseOut.model_validate(item) for item in response.json()]
        except (httpx.HTTPStatusError, ValidationError) as e:
            msg = f"Failed to fetch courses: {e!s}"
            raise CourseRepositoryError(msg) from e

    def get_by_id(self, course_id: str) -> CourseOut:
        """Fetch course by ID from backend API."""
        try:
            response = self._client.get(f"{self._api_path}/{course_id}")
            response.raise_for_status()
            return CourseOut.model_validate(response.json())
        except (httpx.HTTPStatusError, ValidationError) as e:
            msg = f"Failed to fetch course {course_id}: {e!s}"
            raise CourseRepositoryError(msg) from e

    def create(self, course: CourseCreate) -> CourseOut:
        """Create new course via backend API."""
        try:
            response = self._client.post(self._api_path, json=course.model_dump(exclude_none=True))
            response.raise_for_status()
            return CourseOut.model_validate(response.json())
        except (httpx.HTTPStatusError, ValidationError) as e:
            msg = f"Failed to create course: {e!s}"
            raise CourseRepositoryError(msg) from e

    def update(self, course_id: str, course: CourseUpdate) -> CourseOut:
        """Update existing course via backend API."""
        try:
            response = self._client.patch(
                f"{self._api_path}/{course_id}",
                json=course.model_dump(exclude_none=True),
            )
            response.raise_for_status()
            return CourseOut.model_validate(response.json())
        except (httpx.HTTPStatusError, ValidationError) as e:
            msg = f"Failed to update course {course_id}: {e!s}"
            raise CourseRepositoryError(msg) from e

    def delete(self, course_id: str) -> bool:
        """Delete course via backend API."""
        try:
            response = self._client.delete(f"{self._api_path}/{course_id}")
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            msg = f"Failed to delete course {course_id}: {e!s}"
            raise CourseRepositoryError(msg) from e
        else:
            return response.status_code == 204

    def __del__(self):
        """Cleanup HTTP client on deletion."""
        if hasattr(self, "_client"):
            self._client.close()
