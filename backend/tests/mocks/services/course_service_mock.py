from api.models.course import CourseCreate, CourseOut, CourseUpdate
from interfaces.services.course_service import ICourseService


class MockCourseService(ICourseService):
    def get_course(self, course_id):
        return CourseOut(id=course_id, name="Mock Course", cs50_id=50, exercise_ids=[])

    def get_courses(self):
        return [
            CourseOut(id="1", name="Course 1", cs50_id=50, exercise_ids=[]),
            CourseOut(id="2", name="Course 2", cs50_id=51, exercise_ids=[]),
        ]

    def create_course(self, data: CourseCreate):
        return CourseOut(
            id="new_id", name=data.name, cs50_id=data.cs50_id, exercise_ids=data.exercise_ids
        )

    def update_course(self, course_id: str, data: CourseUpdate):
        return CourseOut(
            id=course_id,
            name=data.name,
            cs50_id=data.cs50_id or 50,
            exercise_ids=data.exercise_ids or [],
        )

    def delete_course(self, course_id: str):
        return {"message": f"Course {course_id} deleted"}
