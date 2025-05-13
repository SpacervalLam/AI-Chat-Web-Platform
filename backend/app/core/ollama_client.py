from httpx import AsyncClient, Timeout

from typing import AsyncGenerator, Literal, List, Optional
from pydantic import BaseModel
import json



class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class OllamaChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: bool = False

class OllamaGenerateResponse(BaseModel):
    response: Optional[str] = None 
    created_at: Optional[str] = None
    done: Optional[bool] = None
    id: Optional[str] = None
    object: Optional[str] = None
    model: Optional[str] = None
    usage: Optional[dict] = None

    @classmethod
    def from_raw_response(cls, raw_response: dict):
        return cls(
            response=raw_response.get("message", {}).get("content"),
            created_at=raw_response.get("created_at"),
            done=raw_response.get("done"),
            id=raw_response.get("id"),
            object=raw_response.get("object"),
            model=raw_response.get("model"),
            usage=raw_response.get("usage")
        )

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.timeout = Timeout(connect=None, read=None, write=None, pool=None)
        self.client = AsyncClient(timeout=self.timeout)

    async def list_models(self) -> List[str]:
        """Fetch available model tags from Ollama service."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return [model["name"] for model in response.json().get("models", [])]
        except Exception as e:
            raise Exception(f"Failed to list models: {e}")

    async def chat(
        self,
        model: str,
        messages: List[Message],
        stream: bool = False
    ) -> AsyncGenerator[OllamaGenerateResponse, None]:
        """
        Send a chat request with a sequence of role/content messages.
        Returns an async generator yielding OllamaGenerateResponse chunks.
        """
        url = f"{self.base_url}/api/chat"
        payload = OllamaChatRequest(model=model, messages=messages, stream=stream).dict()

        print(f"[DEBUG] Payload sent to model: {payload}")  # 添加调试日志

        if stream:
            async with self.client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line:
                        print(f"[DEBUG] Raw response line: {line}")  # 添加调试日志
                        yield OllamaGenerateResponse.from_raw_response(json.loads(line))
        else:
            resp = await self.client.post(url, json=payload)
            resp.raise_for_status()
            print(f"[DEBUG] Raw response: {resp.json()}")  # 添加调试日志
            yield OllamaGenerateResponse.from_raw_response(resp.json())

    async def close(self):
        """Close the underlying HTTPX client."""
        await self.client.aclose()
