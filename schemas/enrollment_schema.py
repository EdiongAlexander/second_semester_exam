from pydantic import BaseModel
from datetime import date
from typing import Optional

class EnrollmentSchema(BaseModel):
    user_id: str
    course_id: str

class Enrollment(EnrollmentSchema):
    id: str
    enrolled_date: date
    completed: bool = False

class CreateEnrollment(EnrollmentSchema):
    pass

class UpdateEnrollment(BaseModel):
    user_id: Optional[str] = None
    course_id: Optional[str] = None
    enrolled_date: Optional[date] = None
    completed: Optional[bool] = None

