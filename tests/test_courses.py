from fastapi.testclient import TestClient
from second_semester_exam.main import app

client = TestClient(app)

# Helpers
def create_user(username, email):
    return client.post("/users/", json={
        "username": username,
        "email": email,
        "is_active": True
    }).json()["user"]

def create_course(title, description):
    return client.post("/courses/", json={
        "title": title,
        "description": description
    }).json()["course"]

def enroll_user(user_id, course_id):
    return client.post("/enrollments/", json={
        "user_id": user_id,
        "course_id": course_id
    })

# Test: users in a course
def test_get_users_enrolled_in_course():
    user1 = create_user("alice", "alice@example.com")
    user2 = create_user("bob", "bob@example.com")
    course = create_course("Python 101", "Learn Python")
    enroll_user(user1["id"], course["id"])
    enroll_user(user2["id"], course["id"])

    response = client.get(f"/courses/{course['id']}/users")
    assert response.status_code == 200
    users_in_course = response.json()["users"]
    assert len(users_in_course) == 2
    assert {u["id"] for u in users_in_course} == {user1["id"], user2["id"]}

def create_course(title, description, is_open=True):
    return client.post("/courses/", json={
        "title": title,
        "description": description,
        "is_open": is_open
    }).json()["course"]

def test_create_course():
    response = client.post("/courses/", json={
        "title": "Story of my life",
        "description": "and the story continues",
        "is_open": True
    })
    assert response.status_code == 201
    assert response.json()["course"]["title"] == "Story of my life"

def test_get_courses():
    response = client.get("/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_course_by_id():
    course = create_course("Journey of Ediong", "chapter one begins")
    response = client.get(f"/courses/{course['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Journey of Ediong"

def test_update_course():
    course = create_course("Adventure of Yamma", "a tale worth telling")
    response = client.put(f"/courses/{course['id']}", json={
        "title": "Adventure of Yamma - The Return",
        "description": "chapter two unfolds"
    })
    assert response.status_code == 200
    assert response.json()["course"]["title"] == "Adventure of Yamma - The Return"

def test_close_course():
    course = create_course("Ediong’s Final Quest", "the end is near")
    response = client.put(f"/courses/{course['id']}/close")
    assert response.status_code == 200
    assert response.json()["course"]["is_open"] is False
    

def test_delete_course():
    course = create_course("Yamma’s Hidden Path", "mysteries of the unknown")
    response = client.delete(f"/courses/{course['id']}")
    assert response.status_code == 204
