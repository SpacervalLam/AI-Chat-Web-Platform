from typing import Optional, AsyncGenerator
from ..core.ollama_client import OllamaClient, OllamaGenerateResponse
from ..models.chat_session import ChatSession, Message
from ..schemas.chat import ChatRequest, ChatResponse

class ChatService:
    def __init__(self):
        self.client = OllamaClient()
        self.sessions = {}
        self.default_model = "llama2"

    async def get_available_models(self) -> list[str]:
        return await self.client.list_models()

    async def process_message(self, request: ChatRequest) -> ChatResponse:
        if request.session_id not in self.sessions:
            self.sessions[request.session_id] = ChatSession(
                id=request.session_id,
                messages=[]
            )
        
        session = self.sessions[request.session_id]
        session.messages.append(Message(role="user", content=request.message))

        # 限制会话历史长度
        max_history_length = 50
        if len(session.messages) > max_history_length:
            session.messages = session.messages[-max_history_length:]
        
        model = request.model or self.default_model
        try:
            response = await self.client.generate(
                model=model,
                prompt=request.message,
                stream=False
            )
            session.messages.append(
                Message(role="assistant", content=response.response)
            )
            return ChatResponse(
                message=request.message,
                session_id=request.session_id,
                response=response.response,
                model=model
            )
        except Exception as e:
            print(f"Error during message processing: {e}")  # 添加详细错误日志
            raise

    async def process_message_stream(
        self, 
        request: ChatRequest
    ) -> AsyncGenerator[OllamaGenerateResponse, None]:
        if request.session_id not in self.sessions:
            self.sessions[request.session_id] = ChatSession(
                id=request.session_id,
                messages=[]
            )

        session = self.sessions[request.session_id]
        session.messages.append(Message(role="user", content=request.message))

        # 限制会话历史长度
        max_history_length = 50
        if len(session.messages) > max_history_length:
            session.messages = session.messages[-max_history_length:]

        model = request.model or self.default_model
        try:
            async for response in self.client.generate_stream(
                model=model,
                prompt=request.message
            ):
                yield response
        except Exception as e:
            print(f"Error during stream message processing: {e}")  # 添加详细错误日志
            raise
