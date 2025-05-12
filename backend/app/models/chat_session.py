from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatSession(BaseModel):
    id: str
    messages: List[Message]
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
