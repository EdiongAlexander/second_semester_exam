from fastapi import APIRouter, HTTPException, status
from second_semester_exam.schemas.enrollment_schema import Enrollment, CreateEnrollment, UpdateEnrollment
from second_semester_exam.database import users, courses, enrollments
from uuid import uuid4
from datetime import date

router = APIRouter()

def find_enrollment_by_id(enrollment_id: str):
    for e in enrollments:
        if e.id == enrollment_id:
            return e
    return None

@router.get("/", status_code=status.HTTP_200_OK)
def get_enrollments():
    return enrollments

@router.get("/{enrollment_id}", status_code=status.HTTP_200_OK)
def get_enrollment_by_id(enrollment_id: str):
    for enrollment in enrollments:
        if enrollment.id == enrollment_id:
            return enrollment
    raise HTTPException(status_code=404, detail="Enrollment not found")

@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def get_enrollments_by_user_id(user_id: str):
    user = None
    for u in users:
        if u.id == user_id:
            user = u
            break
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_enrollments = [e for e in enrollments if e.user_id == user_id]
    if not user_enrollments:
        raise HTTPException(status_code=404, detail="No enrollments found for this user")
    return user_enrollments

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment_in: CreateEnrollment):
    user = None
    for u in users:
        if u.id == enrollment_in.user_id:
            user = u
            break

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_active == False:
        raise HTTPException(status_code=400, detail="User is not active")
    
    for e in enrollments:
        if e.user_id == enrollment_in.user_id and e.course_id == enrollment_in.course_id:
            raise HTTPException(status_code=400, detail="User is already enrolled in this course")
    
    course = None
    for c in courses:
        if c.id == enrollment_in.course_id:
            course = c
            break
    if course.is_open == False:
        raise HTTPException(status_code=400, detail="Course is not open for enrollment")
    
    enrollment = Enrollment(
        id=str(uuid4()),
        enrolled_date=date.today(),
        completed=False,
        **enrollment_in.dict()
    )
    enrollments.append(enrollment)
    return {"message": "Enrollment created successfully", "enrollment": enrollment}

@router.put("/{enrollment_id}", status_code=status.HTTP_200_OK)
def update_enrollment(enrollment_id: str, enrollment_in: UpdateEnrollment):
    enrollment = find_enrollment_by_id(enrollment_id)
    if not enrollment:
         raise HTTPException(status_code=404, detail="Enrollment not found")
    
    if enrollment_in.user_id is not None:
        enrollment.user_id = enrollment_in.user_id
    if enrollment_in.course_id is not None:
        enrollment.course_id = enrollment_in.course_id
    if enrollment_in.enrolled_date is not None:
        enrollment.enrolled_date = enrollment_in.enrolled_date
    if enrollment_in.completed is not None:
        enrollment.completed = enrollment_in.completed
    return {"message": "Enrollment updated successfully", "enrollment": enrollment}

@router.put("/{enrollment_id}/completed", status_code=status.HTTP_200_OK)
def completed_enrollment(enrollment_id: str):
    enrollment = find_enrollment_by_id(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment.completed = True
    return {"message": "Enrollment marked as completed", "enrollment": enrollment}

@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: str):
    enrollment = find_enrollment_by_id(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollments.remove(enrollment)
    