import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_models():
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    assert "models" in response.json()

def test_chat_completion():
    response = client.post(
        "/api/v1/completions",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "model": "llama2"
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()

def test_chat_stream():
    response = client.post(
        "/api/v1/completions/stream",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "model": "llama2"
        }
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream"
