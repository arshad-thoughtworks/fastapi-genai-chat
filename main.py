# fastapi/main.py

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
import uvicorn

app = FastAPI()

# In-memory data stores
session_store = []
chat_store = {}

# ------------------- Models -------------------

class SessionCreateRequest(BaseModel):
    session_user: str = Field(..., min_length=1)

class SessionResponse(BaseModel):
    session_id: int
    session_user: str
    created_at: str

class MessageCreateRequest(BaseModel):
    role: str
    content: str = Field(..., min_length=1)

class Message(BaseModel):
    role: str
    content: str

# ------------------- Routes -------------------

@app.post("/sessions", response_model=SessionResponse)
def create_session(request: SessionCreateRequest):
    session_user = request.session_user.strip().lower()
    if not session_user:
        raise HTTPException(status_code=400, detail="Username cannot be empty.")

    session_id = len(session_store) + 1
    created_at = datetime.utcnow().isoformat()

    session = {
        "session_id": session_id,
        "session_user": session_user,
        "created_at": created_at
    }
    session_store.append(session)
    chat_store[session_id] = []

    return session

@app.post("/sessions/{session_id}/messages")
def add_message(
    session_id: int = Path(..., gt=0),
    message: MessageCreateRequest = ...
):
    if session_id not in chat_store:
        raise HTTPException(status_code=404, detail="Session ID not found.")

    if message.role not in ["user", "assistant"]:
        raise HTTPException(status_code=400, detail="Role must be 'user' or 'assistant'.")

    chat_store[session_id].append({
        "role": message.role,
        "content": message.content
    })
    return {"detail": "Message added successfully."}

@app.get("/sessions/{session_id}/messages", response_model=List[Message])
def get_messages(
    session_id: int = Path(..., gt=0),
    role: Optional[str] = Query(None)
):
    if session_id not in chat_store:
        raise HTTPException(status_code=404, detail="Session ID not found.")

    messages = chat_store[session_id]
    if role:
        if role not in ["user", "assistant"]:
            raise HTTPException(status_code=400, detail="Invalid role filter.")
        messages = [msg for msg in messages if msg["role"] == role]
    return messages

# ------------------- Main -------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
