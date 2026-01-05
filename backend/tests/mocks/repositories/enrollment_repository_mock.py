from interfaces.repositories.enrollment_repository_interface import IEnrollmentRepository
from models.enrollment import EnrollmentModel


class MockEnrollmentRepository(IEnrollmentRepository):
    def __init__(self):
        self._data: dict[str, set[str]] = {}  # student_id -> set of course_ids

    def add_enrollment(self, enrollment: EnrollmentModel):
        self._data.setdefault(enrollment.student_id, set()).add(enrollment.course_id)

    def add_bulk_enrollments(self, enrollments: list[EnrollmentModel]):
        for enrollment in enrollments:
            self.add_enrollment(enrollment)

    def get_courses_for_student(self, student_id: str) -> list[str]:
        return list(self._data.get(student_id, set()))

    def get_students_for_course(self, course_id: str) -> list[str]:
        return [student_id for student_id, courses in self._data.items() if course_id in courses]

    def remove_enrollment(self, enrollment: EnrollmentModel) -> bool:
        student_courses = self._data.get(enrollment.student_id)

        if not student_courses or enrollment.course_id not in student_courses:
            return False

        student_courses.remove(enrollment.course_id)

        # cleanup the dict if empty
        if not student_courses:
            self._data.pop(enrollment.student_id)

        return True
