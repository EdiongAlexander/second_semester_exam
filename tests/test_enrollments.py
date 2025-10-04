from fastapi.testclient import TestClient
from second_semester_exam.main import app

client = TestClient(app)


def create_user(username, email):
    return client.post("/users/", json={
        "username": username,
        "email": email,
        "is_active": True
    }).json()["user"]


def create_course(title, description):
    return client.post("/courses/", json={
        "title": title,
        "description": description,
        "is_open": True
    }).json()["course"]


def test_create_enrollment():
    user = create_user("ediong", "ediong_enroll@example.com")
    course = create_course("Yamma’s Long Walk", "a journey through the desert")

    response = client.post("/enrollments/", json={
        "user_id": user["id"],
        "course_id": course["id"]
    })
    assert response.status_code == 201
    assert response.json()["enrollment"]["user_id"] == user["id"]


def test_get_enrollments():
    response = client.get("/enrollments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_enrollment_by_id():
    user = create_user("yamma", "yamma_enroll@example.com")
    course = create_course("The Chronicles of Ediong", "from the beginning to the end")

    enrollment = client.post("/enrollments/", json={
        "user_id": user["id"],
        "course_id": course["id"]
    }).json()["enrollment"]

    response = client.get(f"/enrollments/{enrollment['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == enrollment["id"]


def test_get_enrollments_by_user_id():
    user = create_user("ediong", "ediong_user_enroll@example.com")
    course = create_course("Tales of Yamma", "legends never die")

    client.post("/enrollments/", json={
        "user_id": user["id"],
        "course_id": course["id"]
    })

    response = client.get(f"/enrollments/user/{user['id']}")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_update_enrollment():
    user = create_user("yamma", "yamma_update_enroll@example.com")
    course = create_course("Story of Destiny", "a fate sealed in stars")

    enrollment = client.post("/enrollments/", json={
        "user_id": user["id"],
        "course_id": course["id"]
    }).json()["enrollment"]

    new_course = create_course("New Dawn", "a fresh beginning")

    response = client.put(f"/enrollments/{enrollment['id']}", json={
        "course_id": new_course["id"]
    })
    assert response.status_code == 200
    assert response.json()["enrollment"]["course_id"] == new_course["id"]


def test_enrollment_completed():
    user = create_user("ediong", "ediong_complete@example.com")
    course = create_course("Final Steps", "closing the circle")

    enrollment = client.post("/enrollments/", json={
        "user_id": user["id"],
        "course_id": course["id"]
    }).json()["enrollment"]

    response = client.put(f"/enrollments/{enrollment['id']}/completed")
    assert response.status_code == 200
    assert response.json()["enrollment"]["completed"] is True


def test_delete_enrollment():
    user = create_user("yamma", "yamma_delete_enroll@example.com")
    course = create_course("Forgotten Paths", "roads less traveled")

    enrollment = client.post("/enrollments/", json={
        "user_id": user["id"],
        "course_id": course["id"]
    }).json()["enrollment"]

    response = client.delete(f"/enrollments/{enrollment['id']}")
    assert response.status_code == 204
