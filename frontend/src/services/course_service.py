
import os
from typing import Any

import requests

from interfaces.services import CourseServiceInterface


class CourseServiceError(Exception):
    """Custom exception for CourseService errors."""


class CourseService(CourseServiceInterface):
    """Service to handle course-related API calls to the backend."""

    def __init__(self) -> None:
        """Initialize the CourseService with backend URL configuration."""
        self.base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.api_url = f"{self.base_url}/api/v1/courses"

    def get_courses(self) -> list[dict[str, Any]]:
        """Fetch all courses from the backend."""
        try:
            response = requests.get(self.api_url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"Failed to fetch courses: {e!s}"
            raise CourseServiceError(msg) from e

    def get_course(self, course_id: str) -> dict[str, Any]:
        """Fetch a single course by ID from the backend."""
        try:
            response = requests.get(f"{self.api_url}/{course_id}", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"Failed to fetch course: {e!s}"
            raise CourseServiceError(msg) from e

    def create_course(self, name: str, cs50_id: int | None = None) -> dict[str, Any]:
        """Create a new course."""
        try:
            data: dict[str, Any] = {"name": name}
            if cs50_id is not None:
                data["cs50_id"] = cs50_id

            response = requests.post(self.api_url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            msg = f"Failed to create course: {e!s}"
            raise CourseServiceError(msg) from e
