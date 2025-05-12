from pydantic import BaseModel
from typing import List, Optional

class ChatSession(BaseModel):
    id: str
    messages: List[dict]  # 直接使用字典表示消息，包含 role 和 content
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
