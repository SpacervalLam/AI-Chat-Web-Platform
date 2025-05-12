from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.core.ollama_client import OllamaClient
from app.schemas.chat import ChatRequest
from typing import AsyncGenerator
import json

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

        model = request.model or "llama2"
        prompt = request.messages[0].content if request.messages else ""
        print(f"[DEBUG] Using model: {model}, Prompt: {prompt}")

        response = await ollama.generate(
            model=model,
            prompt=prompt,
            stream=False
        )

        print(f"[DEBUG] Generated response: {response}")

        return {"response": response.response, "model": model}
    except Exception as e:

        import traceback
        error_details = traceback.format_exc()
        print(f"[ERROR] Error during chat    generation: {e}\n{error_details}")
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")
    finally:
        print("[DEBUG] Chat endpoint execution completed.")

@router.post("/completions/stream")
async def chat_stream(request: ChatRequest):
    async def generate_chat_stream(request: ChatRequest) -> AsyncGenerator[str, None]:
        try:
            model = request.model or "llama2"  
            async for chunk in ollama.generate_stream(
                model=model,
                prompt=request.message
            ):
                yield f"data: {json.dumps({'response': chunk.response, 'model': model})}\n\n"
        except Exception as e:
            print(f"Error during stream generation: {e}") 
            yield f"data: {json.dumps({'error': 'Failed to generate response'})}\n\n"

    return StreamingResponse(
        generate_chat_stream(request),
        media_type="text/event-stream"
    )
