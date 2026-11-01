Chat Router
from fastapi import APIRouter, Depends
from typing import Dict, Any

from src.core.common import success_response
from .service import ChatService
from .schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

def get_chat_service() -> ChatService:
    return ChatService()

@router.post("", response_model=Dict[str, Any])
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service)
) -> Dict[str, Any]:
    Chat with calculator agent
    
    Agent có thể:
    - Cộng, trừ, nhân, chia các số
    - Xử lý các phép tính phức tạp
    - Trả lời bằng tiếng Việt
    
    Example requests:
    - "Tính 25 * 4 + 10"
    - "15 chia for 3 bằng bao nhiêu?"
    - "(100 - 20) * 2"
    result = await service.chat(request)
    
    return success_response(
        data=result.model_dump(),
        meta={
            "conversation_id": result.conversation_id
        }
    )

@router.get("/tools", response_model=Dict[str, Any])
async def list_tools(
    service: ChatService = Depends(get_chat_service)
) -> Dict[str, Any]:
    Liệt kê all tools mà agent có thể sử dụng
    
    Returns:
        List of available tools with descriptions
    result = await service.list_tools()
    return success_response(data=result)
