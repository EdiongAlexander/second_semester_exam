from fastapi import APIRouter, status
from second_semester_exam.schemas.enrollment_schema import CreateEnrollment, UpdateEnrollment
from second_semester_exam.services.enrollment_service import (
    get_enrollments,
    get_enrollment_by_id,
    get_enrollments_by_user_id,
    create_enrollment,
    update_enrollment,
    completed_enrollment,
    delete_enrollment,
)

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def route_get_enrollments():
    return get_enrollments()


@router.get("/{enrollment_id}", status_code=status.HTTP_200_OK)
def route_get_enrollment_by_id(enrollment_id: str):
    return get_enrollment_by_id(enrollment_id)


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def route_get_enrollments_by_user_id(user_id: str):
    return get_enrollments_by_user_id(user_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def route_create_enrollment(enrollment_in: CreateEnrollment):
    enrollment = create_enrollment(enrollment_in)
    return {"message": "Enrollment created successfully", "enrollment": enrollment}


@router.put("/{enrollment_id}", status_code=status.HTTP_200_OK)
def route_update_enrollment(enrollment_id: str, enrollment_in: UpdateEnrollment):
    enrollment = update_enrollment(enrollment_id, enrollment_in)
    return {"message": "Enrollment updated successfully", "enrollment": enrollment}


@router.put("/{enrollment_id}/completed", status_code=status.HTTP_200_OK)
def route_completed_enrollment(enrollment_id: str):
    enrollment = completed_enrollment(enrollment_id)
    return {"message": "Enrollment marked as completed", "enrollment": enrollment}


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def route_delete_enrollment(enrollment_id: str):
    delete_enrollment(enrollment_id)
