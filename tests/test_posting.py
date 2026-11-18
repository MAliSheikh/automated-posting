from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_message_too_long():
    response = client.post("/posting", json={"message": "a" * 201 + " https://example.com"})
    assert response.status_code == 422


def test_no_link():
    response = client.post("/posting", json={"message": "Hello world"})
    assert response.status_code == 422


def test_two_links():
    response = client.post(
        "/posting", json={"message": "https://a.com and https://b.com"}
    )
    assert response.status_code == 422


def test_invalid_url():
    response = client.post("/posting", json={"message": "Visit https://nodot now"})
    assert response.status_code == 422