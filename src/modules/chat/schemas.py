Chat module schemas
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ChatRequest(BaseModel):
    message: str = Field(..., description="Tin nhắn từ user", min_length=1)
    conversation_id: Optional[str] = Field(
        None,
        description="ID of conversation (để duy trì context)"
    )
    
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
    conversation_id: str = Field(..., description="ID of conversation")
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Thông tin bổ sung"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response": "Kết quả là 110",
                    "conversation_id": "conv_123",
                    "metadata": {
                        "steps": 2,
                        "tools_used": ["multiply", "add"],
                        "provider": "openai"
                    }
                }
            ]
        }
    }
