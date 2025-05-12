import httpx
from typing import AsyncGenerator
from pydantic import BaseModel
from typing import Optional
from typing import List
import json

class OllamaGenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = False
    context: Optional[List[int]] = None

class OllamaGenerateResponse(BaseModel):
    model: str
    created_at: str
    response: str
    done: bool
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def list_models(self) -> List[str]:
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return [model["name"] for model in response.json().get("models", [])]
        except Exception as e:
            raise Exception(f"Failed to list models: {str(e)}")

    async def generate(
        self, 
        model: str, 
        prompt: str, 
        stream: bool = False
    ) -> OllamaGenerateResponse:
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": stream
                }
            )
            response.raise_for_status()
            return OllamaGenerateResponse(**response.json())
        except Exception as e:
            raise Exception(f"Generation failed: {str(e)}")

    async def generate_stream(
        self, 
        model: str, 
        prompt: str
    ) -> AsyncGenerator[OllamaGenerateResponse, None]:
        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True
                }
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        yield OllamaGenerateResponse(**json.loads(line))
        except Exception as e:
            raise Exception(f"Stream generation failed: {str(e)}")
