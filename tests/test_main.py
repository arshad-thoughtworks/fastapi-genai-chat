import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

# ---------- Test Data ----------
valid_user = {"session_user": " Arshad "}
invalid_user = {"session_user": "   "}
valid_message = {"role": "user", "content": "What is AI?"}
invalid_role_message = {"role": "human", "content": "Hey"}

# ---------- Tests ----------

def test_create_session_success():
    response = client.post("/sessions", json=valid_user)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == 1
    assert data["session_user"] == "arshad"
    assert "created_at" in data

def test_create_session_failure():
    response = client.post("/sessions", json=invalid_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username cannot be empty."

def test_add_message_success():
    client.post("/sessions", json=valid_user)  # Ensure session exists
    response = client.post("/sessions/1/messages", json=valid_message)
    assert response.status_code == 200
    assert response.json()["detail"] == "Message added successfully."

def test_add_message_invalid_session():
    response = client.post("/sessions/999/messages", json=valid_message)
    assert response.status_code == 404
    assert response.json()["detail"] == "Session ID not found."

def test_add_message_invalid_role():
    client.post("/sessions", json=valid_user)
    response = client.post("/sessions/1/messages", json=invalid_role_message)
    assert response.status_code == 400
    assert response.json()["detail"] == "Role must be 'user' or 'assistant'."

def test_get_messages():
    client.post("/sessions", json=valid_user)
    client.post("/sessions/1/messages", json=valid_message)
    response = client.get("/sessions/1/messages")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["role"] == "user"
    assert data[0]["content"] == "What is AI?"

def test_get_messages_invalid_session():
    response = client.get("/sessions/999/messages")
    assert response.status_code == 404
    assert response.json()["detail"] == "Session ID not found."

def test_get_messages_filter_by_role():
    client.post("/sessions", json=valid_user)
    client.post("/sessions/1/messages", json=valid_message)
    response = client.get("/sessions/1/messages?role=user")
    assert response.status_code == 200
    data = response.json()
    assert all(msg["role"] == "user" for msg in data)
