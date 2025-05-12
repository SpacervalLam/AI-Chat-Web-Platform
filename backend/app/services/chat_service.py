from typing import Optional, AsyncGenerator
from ..core.ollama_client import OllamaClient, OllamaGenerateResponse
from ..models.chat_session import ChatSession  
from ..schemas.chat import ChatRequest, ChatResponse

class ChatService:
    def __init__(self):
        self.client = OllamaClient()
        self.sessions = {}
        self.default_model = ""

    async def get_available_models(self) -> list[str]:
        return await self.client.list_models()

    async def process_message(self, request: ChatRequest) -> ChatResponse:
        # 获取会话或创建新的会话
        if request.session_id not in self.sessions:
            self.sessions[request.session_id] = ChatSession(
                id=request.session_id,
                messages=[]
            )
        
        session = self.sessions[request.session_id]

        # 遍历请求中的消息
        for user_message in request.messages:
            session.messages.append(user_message)  # 直接添加消息字典

        # 限制会话历史长度
        max_history_length = 50
        if len(session.messages) > max_history_length:
            session.messages = session.messages[-max_history_length:]

        model = request.model or self.default_model

        try:
            # 处理多个消息的响应
            response_content = ""
            for user_message in request.messages:
                response = await self.client.generate(
                    model=model,
                    prompt=user_message['content'],
                    stream=False
                )
                response_content += response.response + " "  # 将多个响应合并

            # 添加助理的响应
            session.messages.append({
                'role': 'assistant', 
                'content': response_content.strip()
            })
            
            return ChatResponse(
                message=request.messages[-1]['content'],  # 返回最新一条消息
                session_id=request.session_id,
                response=response_content.strip(),
                model=model
            )

        except Exception as e:
            print(f"Error during message processing: {e}")
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

        # 遍历请求中的消息
        for user_message in request.messages:
            session.messages.append(user_message)  # 直接添加消息字典

        # 限制会话历史长度
        max_history_length = 50
        if len(session.messages) > max_history_length:
            session.messages = session.messages[-max_history_length:]

        model = request.model or self.default_model

        try:
            # 处理消息流
            for user_message in request.messages:
                async for response in self.client.generate_stream(
                    model=model,
                    prompt=user_message['content']
                ):
                    yield response
        except Exception as e:
            print(f"Error during stream message processing: {e}")
            raise
