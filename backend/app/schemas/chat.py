from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    model: Optional[str] = None
    messages: List[dict] 

class ChatResponse(BaseModel):
    message: str
    session_id: str
    response: str
    status: str = "success"
