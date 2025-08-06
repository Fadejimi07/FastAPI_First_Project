from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_posts():
    response = client.get("/blog/all")
    assert response.status_code == 200


def test_auth_error():
    response = client.post("/token", data={"username": "", "password": ""})
    access_token = response.json().get("access_token")
    assert access_token is None
    details = response.json().get("detail")
    # Handle both error response formats
    if isinstance(details, list):
        message = details[0].get("msg")
        assert message == "Field required"
    else:
        assert details == "Invalid credentials"


def test_auth_success():
    response = client.post(
        "/token", data={"username": "fadmantest2", "password": "password"}
    )
    access_token = response.json().get("access_token")
    assert access_token is not None


def test_post_article():
    auth = client.post(
        "/token", data={"username": "fadmantest2", "password": "password"}
    )
    access_token = auth.json().get("access_token")
    assert access_token

    response = client.post(
        "/article/",
        json={
            "title": "Test Article",
            "content": "This is a test article.",
            "published": True,
            "creator_id": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json().get("title") == "Test Article"
    assert response.json().get("content") == "This is a test article."
    assert response.json().get("published") is True
