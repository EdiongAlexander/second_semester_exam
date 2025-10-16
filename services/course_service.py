from fastapi import HTTPException
from schemas.course_schema import Course, CreateCourse, UpdateCourse
from database import users, courses, enrollments
from uuid import uuid4


def find_course_by_id(course_id: str):
    for c in courses:
        if c.id == course_id:
            return c
    return None


def get_courses():
    return courses


def get_course_by_id(course_id: str):
    for c in courses:
        if c.id == course_id:
            return c
    raise HTTPException(status_code=404, detail="Course not found")


def get_users_enrolled_in_course(course_id: str):
    course = find_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    enrolled = [e for e in enrollments if e.course_id == course_id]
    enrolled_users = [user for user in users if any(e.user_id == user.id for e in enrolled)]
    return enrolled_users


def create_course(course_in: CreateCourse):
    course = Course(
        id=str(uuid4()),
        is_open=True,
        **course_in.dict()
    )
    courses.append(course)
    return course


def update_course(course_id: str, course_in: UpdateCourse):
    course = find_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course_in.title is not None:
        course.title = course_in.title
    if course_in.description is not None:
        course.description = course_in.description
    if course_in.is_open is not None:
        course.is_open = course_in.is_open
    return course


def close_course(course_id: str):
    course = find_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.is_open = False
    return course


def delete_course(course_id: str):
    course = find_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    courses.remove(course)
    return course
