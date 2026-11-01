"""
Pydantic models cho API requests/responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatMessage(BaseModel):
    """Một message trong conversation"""
    role: str = Field(..., description="Vai trò: 'user', 'assistant', hoặc 'system'")
    content: str = Field(..., description="Nội dung message")


class ChatRequest(BaseModel):
    """Request để chat với agent"""
    message: str = Field(..., description="Tin nhắn từ user", min_length=1)
    conversation_id: Optional[str] = Field(None, description="ID của conversation (để duy trì context)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Tính 25 * 4 + 10",
                    "conversation_id": "conv_123"
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """Response từ agent"""
    response: str = Field(..., description="Câu trả lời từ agent")
    conversation_id: str = Field(..., description="ID của conversation")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Thông tin bổ sung")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response": "Kết quả là 110",
                    "conversation_id": "conv_123",
                    "metadata": {
                        "steps": 2,
                        "tools_used": ["multiply", "add"]
                    }
                }
            ]
        }
    }


class AgentState(BaseModel):
    """State của agent trong LangGraph"""
    messages: List[ChatMessage] = Field(default_factory=list, description="Lịch sử messages")
    current_step: int = Field(0, description="Bước hiện tại trong workflow")
    tool_calls: int = Field(0, description="Số lần gọi tools")
