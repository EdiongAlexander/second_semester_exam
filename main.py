from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from second_semester_exam.routers.users import router as users_router
from second_semester_exam.routers.courses import router as courses_router
from second_semester_exam.routers.enrollments import router as enrollments_router



app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(enrollments_router, prefix="/enrollments", tags=["enrollments"])
app.include_router(courses_router, prefix="/courses", tags=["courses"])

@app.get("/", status_code=200)
def home():
    return "Second semester exams!"


