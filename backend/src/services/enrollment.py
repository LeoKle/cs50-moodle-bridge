from typing import BinaryIO

import pandas as pd

from exceptions.exceptions import CourseDoesNotExistException, InvalidCsvFormat
from interfaces.repositories.course_repository_interface import ICourseRepository
from interfaces.repositories.enrollment_repository_interface import IEnrollmentRepository
from interfaces.repositories.student_repository_interface import IStudentRepository
from interfaces.services.enrollment_service import EnrollmentImportResult, IEnrollmentService
from models.enrollment import EnrollmentModel
from models.student import StudentModel


class EnrollmentService(IEnrollmentService):
    def __init__(
        self,
        student_repository: IStudentRepository,
        course_repository: ICourseRepository,
        enrollment_repository: IEnrollmentRepository,
    ):
        self._student_repo = student_repository
        self._course_repo = course_repository
        self._enroll_repo = enrollment_repository

    def import_students_from_csv(self, course_id: str, file: BinaryIO):
        course = self._course_repo.get(course_id)
        if not course:
            raise CourseDoesNotExistException

        df = pd.read_csv(file)

        required_columns = {"Vorname", "Nachname", "E-Mail-Adresse"}
        if not required_columns.issubset(df.columns):
            raise InvalidCsvFormat

        students_created = 0
        enrollments_created = 0
        rows_skipped = 0

        for _, row in df.iterrows():
            email = str(row["E-Mail-Adresse"]).strip()
            first_name = str(row["Vorname"]).strip()
            last_name = str(row["Nachname"]).strip()

            if not email or email == "nan":
                rows_skipped += 1
                continue

            student = self._student_repo.get_by_email(email)

            if not student:
                student = StudentModel(
                    email=email,
                    name=f"{first_name} {last_name}",
                )
                self._student_repo.create(student)
                students_created += 1

            self._enroll_repo.add_enrollment(
                EnrollmentModel(student_id=student.id, course_id=course_id)
            )
            enrollments_created += 1

        return EnrollmentImportResult(
            students_created=students_created,
            enrollments_created=enrollments_created,
            rows_skipped=rows_skipped,
        )
