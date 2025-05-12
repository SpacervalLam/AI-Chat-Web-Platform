from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.core.ollama_client import OllamaClient
from app.schemas.chat import ChatRequest
from typing import AsyncGenerator
import json
import traceback

router = APIRouter()
ollama = OllamaClient()

@router.get("/models")
async def list_models():
    try:
        models = await ollama.list_models()
        return {"models": models}
    except Exception as e:
        print(f"Error fetching models: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch models")

@router.post("/completions")
async def chat(request: ChatRequest):
    try:
        print(f"[DEBUG] Received request: {request}")

        if not request.messages:
            raise HTTPException(status_code=400, detail="Messages array cannot be empty")

        model = request.model
        print(f"[DEBUG] Using model: {model}")

        response_data = ""
        async for chunk in ollama.chat(
            model=model,
            messages=request.messages,
            stream=False
        ):
            print(f"[DEBUG] Chunk response: {chunk.response}")  # 添加调试日志
            response_data += chunk.response or ""

        return {"response": response_data, "model": model}
    except Exception as e:
        import traceback
        print(f"[ERROR] Error during chat generation: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to generate response")


@router.post("/completions/stream")
async def chat_stream(request: ChatRequest):
    async def generate_chat_stream(request: ChatRequest) -> AsyncGenerator[str, None]:
        try:
            model = request.model

            async for chunk in ollama.chat(
                model=model,
                messages=request.messages,
                stream=True
            ):
                yield f"data: {json.dumps({'response': chunk.response, 'model': model})}\n\n"

        except Exception as e:
            import traceback
            print(f"[ERROR] Error during stream generation: {e}\n{traceback.format_exc()}")
            yield f"data: {json.dumps({'error': 'Failed to generate response'})}\n\n"

    return StreamingResponse(
        generate_chat_stream(request),
        media_type="text/event-stream"
    )

