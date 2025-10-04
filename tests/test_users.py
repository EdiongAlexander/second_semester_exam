from fastapi.testclient import TestClient
from second_semester_exam.main import app

client = TestClient(app)


def test_create_user():
    response = client.post("/users/", json={
        "username": "ediong",
        "email": "ediong@example.com",
        "is_active": True
    })
    assert response.status_code == 201
    assert response.json()["user"]["username"] == "ediong"


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id():
    user = client.post("/users/", json={
        "username": "yamma",
        "email": "yamma@example.com",
        "is_active": True
    }).json()["user"]

    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    assert response.json()["username"] == "yamma"


def test_update_user():
    user = client.post("/users/", json={
        "username": "ediong",
        "email": "ediong_update@example.com",
        "is_active": True
    }).json()["user"]

    response = client.put(f"/users/{user['id']}", json={
        "username": "yamma"
    })
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "yamma"


def test_deactivate_user():
    user = client.post("/users/", json={
        "username": "ediong",
        "email": "ediong_deactivate@example.com",
        "is_active": True
    }).json()["user"]

    response = client.put(f"/users/{user['id']}/deactivate")
    assert response.status_code == 200
    assert response.json()["user"]["is_active"] is False


def test_delete_user():
    user = client.post("/users/", json={
        "username": "yamma",
        "email": "delete_yamma@example.com",
        "is_active": True
    }).json()["user"]

    response = client.delete(f"/users/{user['id']}")
    assert response.status_code == 204
