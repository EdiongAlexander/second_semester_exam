from fastapi import APIRouter, status
from schemas.course_schema import CreateCourse, UpdateCourse
from services.course_service import (
    get_courses,
    get_course_by_id,
    get_users_enrolled_in_course,
    create_course,
    update_course,
    close_course,
    delete_course,
)

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_courses_route():
    return get_courses()


@router.get("/{course_id}", status_code=status.HTTP_200_OK)
def get_course_by_id_route(course_id: str):
    return get_course_by_id(course_id)


@router.get("/{course_id}/users", status_code=status.HTTP_200_OK)
def get_users_enrolled_in_course_route(course_id: str):
    users = get_users_enrolled_in_course(course_id)
    return {"message": "Users fetched successully", "users": users}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course_route(course_in: CreateCourse):
    course = create_course(course_in)
    return {"message": "Course created successfully", "course": course}


@router.put("/{course_id}", status_code=status.HTTP_200_OK)
def update_course_route(course_id: str, course_in: UpdateCourse):
    course = update_course(course_id, course_in)
    return {"message": "Course updated successfully", "course": course}


@router.put("/{course_id}/close", status_code=status.HTTP_200_OK)
def close_course_route(course_id: str):
    course = close_course(course_id)
    return {"message": "Course closed successfully", "course": course}


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_route(course_id: str):
    delete_course(course_id)
