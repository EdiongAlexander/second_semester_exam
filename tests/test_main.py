from fastapi.testclient import TestClient
from second_semester_exam.main import app


client = TestClient(app)

def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200