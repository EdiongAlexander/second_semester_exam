from fastapi.testclient import TestClient
from second_semester_exam.main import app
from datetime import date

client = TestClient(app)

# Helpers
def create_user(username, email, is_active=True):
    return client.post("/users/", json={
        "username": username,
        "email": email,
        "is_active": is_active
    }).json()["user"]

def create_course(title, description, is_open=True):
    return client.post("/courses/", json={
        "title": title,
        "description": description,
        "is_open": is_open
    }).json()["course"]

def enroll_user(user_id, course_id):
    return client.post("/enrollments/", json={
        "user_id": user_id,
        "course_id": course_id
    })

# Enrollment CRUD & completion
def test_create_enrollment():
    user = create_user("ediong", "ediong_enroll@example.com")
    course = create_course("Yamma’s Long Walk", "a journey through the desert")
    response = enroll_user(user["id"], course["id"])
    assert response.status_code == 201
    assert response.json()["enrollment"]["user_id"] == user["id"]

def test_get_enrollments():
    response = client.get("/enrollments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_enrollment_by_id():
    user = create_user("yamma", "yamma_enroll@example.com")
    course = create_course("The Chronicles of Ediong", "from the beginning to the end")
    enrollment = enroll_user(user["id"], course["id"]).json()["enrollment"]
    response = client.get(f"/enrollments/{enrollment['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == enrollment["id"]

def test_get_enrollments_by_user_id():
    user = create_user("ediong", "ediong_user_enroll@example.com")
    course = create_course("Tales of Yamma", "legends never die")
    enroll_user(user["id"], course["id"])
    response = client.get(f"/enrollments/user/{user['id']}")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_enrollment():
    user = create_user("yamma", "yamma_update_enroll@example.com")
    course = create_course("Story of Destiny", "a fate sealed in stars")
    enrollment = enroll_user(user["id"], course["id"]).json()["enrollment"]
    new_course = create_course("New Dawn", "a fresh beginning")
    response = client.put(f"/enrollments/{enrollment['id']}", json={"course_id": new_course["id"]})
    assert response.status_code == 200
    assert response.json()["enrollment"]["course_id"] == new_course["id"]

def test_enrollment_completed():
    user = create_user("ediong", "ediong_complete@example.com")
    course = create_course("Final Steps", "closing the circle")
    enrollment = enroll_user(user["id"], course["id"]).json()["enrollment"]
    response = client.put(f"/enrollments/{enrollment['id']}/completed")
    assert response.status_code == 200
    assert response.json()["enrollment"]["completed"] is True

def test_delete_enrollment():
    user = create_user("yamma", "yamma_delete_enroll@example.com")
    course = create_course("Forgotten Paths", "roads less traveled")
    enrollment = enroll_user(user["id"], course["id"]).json()["enrollment"]
    response = client.delete(f"/enrollments/{enrollment['id']}")
    assert response.status_code == 204

# Enrollment validation & extra features
def test_inactive_user_cannot_enroll():
    inactive_user = create_user("charlie", "charlie@example.com", is_active=False)
    course = create_course("Inactive User Test", "Testing inactive user")
    response = enroll_user(inactive_user["id"], course["id"])
    assert response.status_code == 400
    assert response.json()["detail"] == "User is not active"

def test_cannot_enroll_in_closed_course():
    user = create_user("dave", "dave@example.com")
    course = create_course("Closed Course", "Course is closed")
    
    client.put(f"/courses/{course['id']}/close")
    
    response = enroll_user(user["id"], course["id"])
    assert response.status_code == 400
    assert response.json()["detail"] == "Course is not open for enrollment"


def test_user_cannot_enroll_twice():
    user = create_user("eve", "eve@example.com")
    course = create_course("Unique Enrollment", "User cannot enroll twice")
    enroll_user(user["id"], course["id"])
    response = enroll_user(user["id"], course["id"])
    assert response.status_code == 400
    assert response.json()["detail"] == "User is already enrolled in this course"

def test_enrollment_has_date():
    user = create_user("frank", "frank@example.com")
    course = create_course("Date Test Course", "Check enrollment date")
    response = enroll_user(user["id"], course["id"])
    assert response.status_code == 201
    enrollment = response.json()["enrollment"]
    assert "enrolled_date" in enrollment
    enrolled_date = date.fromisoformat(enrollment["enrolled_date"])
    assert enrolled_date == date.today()
