import os
import requests
from typing import List, Dict, Any


class CourseService:
    """Service to handle course-related API calls to the backend."""

    def __init__(self):
        self.base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.api_url = f"{self.base_url}/api/v1/courses"

    def get_courses(self) -> List[Dict[str, Any]]:
        """Fetch all courses from the backend."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch courses: {str(e)}")

    def get_course(self, course_id: str) -> Dict[str, Any]:
        """Fetch a single course by ID from the backend."""
        try:
            response = requests.get(f"{self.api_url}/{course_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch course: {str(e)}")

    def create_course(self, name: str, cs50_id: int | None = None) -> Dict[str, Any]:
        """Create a new course."""
        try:
            data = {"name": name}
            if cs50_id is not None:
                data["cs50_id"] = cs50_id
            
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create course: {str(e)}")
