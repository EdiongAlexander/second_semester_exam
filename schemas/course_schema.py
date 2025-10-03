from pydantic import BaseModel
from typing import Optional

class CourseSchema(BaseModel):
    title: str
    description: str

class Course(CourseSchema):
    id: str
    is_open: bool = True

class CreateCourse(CourseSchema):
    pass

class UpdateCourse(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_open: Optional[bool] = None