from pydantic import BaseModel


class EnrollmentModel(BaseModel):
    student_id: str
    course_id: str
