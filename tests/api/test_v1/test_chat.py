import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.get("/api/v1/chat")
    assert response.status_code == 200
    assert response.json() == {"message": "Chat endpoint"}

def test_chat_post_message():
    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
