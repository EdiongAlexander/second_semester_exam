from fastapi.testclient import TestClient
from second_semester_exam.main import app

client = TestClient(app)


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
    course = client.post("/courses/", json={
        "title": "Journey of Ediong",
        "description": "chapter one begins",
        "is_open": True
    }).json()["course"]

    response = client.get(f"/courses/{course['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Journey of Ediong"


def test_update_course():
    course = client.post("/courses/", json={
        "title": "Adventure of Yamma",
        "description": "a tale worth telling",
        "is_open": True
    }).json()["course"]

    response = client.put(f"/courses/{course['id']}", json={
        "title": "Adventure of Yamma - The Return",
        "description": "chapter two unfolds"
    })
    assert response.status_code == 200
    assert response.json()["course"]["title"] == "Adventure of Yamma - The Return"


def test_close_course():
    course = client.post("/courses/", json={
        "title": "Ediong’s Final Quest",
        "description": "the end is near",
        "is_open": True
    }).json()["course"]

    response = client.put(f"/courses/{course['id']}/close")
    assert response.status_code == 200
    assert response.json()["course"]["is_open"] is False


def test_delete_course():
    course = client.post("/courses/", json={
        "title": "Yamma’s Hidden Path",
        "description": "mysteries of the unknown",
        "is_open": True
    }).json()["course"]

    response = client.delete(f"/courses/{course['id']}")
    assert response.status_code == 204

