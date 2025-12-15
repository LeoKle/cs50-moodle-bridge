from copy import deepcopy

from interfaces.services.course_service import ICourseService
from models.course import Course


class MockCourseService(ICourseService):
    def __init__(self):
        self._courses: dict[str, Course] = {}

    def get_course(self, course_id):
        course = self._courses.get(course_id)

        if course is None:
            return None
        return course.model_copy(deep=True)

    def get_courses(self):
        return [c.model_copy(deep=True) for c in self._courses.values()]

    def create_course(self, data: Course):
        self._courses[data.id] = data.model_copy(deep=True)
        return self._courses[data.id].model_copy(deep=True)

    def update_course(self, course_id: str, data: Course):
        if course_id not in self._courses:
            return None

        updated = Course(
            id=course_id,
            name=data.name,
            cs50_id=data.cs50_id or self._courses[course_id].cs50_id,
            exercise_ids=deepcopy(data.exercise_ids) or [],
        )
        self._courses[course_id] = updated
        return self._courses[course_id].model_copy(deep=True)

    def delete_course(self, course_id: str):
        return self._courses.pop(course_id, None) is not None
