from interfaces.repositories.course_repository_interface import ICourseRepository
from interfaces.services.course_service import ICourseService
from models.course import Course


class CourseService(ICourseService):
    def __init__(self, course_repository: ICourseRepository):
        self.course_repository = course_repository

    def get_course(self, course_id: str) -> Course | None:
        record = self.course_repository.get(course_id)
        if record is None:
            return None
        return record

    def get_courses(self) -> list[Course]:
        records = self.course_repository.get_all()
        return records

    def create_course(self, data: Course) -> Course:
        created = self.course_repository.create(data)
        return created

    def update_course(self, course_id: str, data: Course) -> Course | None:
        updated = self.course_repository.update(course_id, data)
        if updated is None:
            return None

        return updated

    def delete_course(self, course_id: str) -> bool:
        return self.course_repository.delete(course_id)
