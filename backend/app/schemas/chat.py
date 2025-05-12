from pydantic import BaseModel
from typing import Optional
from typing import List

class ChatMessage(BaseModel):
    role: str  # e.g., "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = "llama2"
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    message: str
    session_id: str
    response: str
    status: str = "success"
