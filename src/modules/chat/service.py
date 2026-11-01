Chat Service - Business logic for chat
from typing import Dict, Any
import uuid
import logging

from src.core.common import AgentError, LLMError
from .schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

class ChatService:
    Service layer for functionality
    
    Separate business logic khỏi HTTP layer
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        Process chat request with agent
        
        Args:
            request: Chat request
            
        Returns:
            Chat response
            
        Raises:
            AgentError: Nếu agent execution fails
            LLMError: Nếu LLM provider fails
        # Generate conversation ID if chưa có
        conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        
        logger.info(
            f"Processing chat request",
            extra={
                "conversation_id": conversation_id,
                "message_length": len(request.message)
            }
        )
        
        try:
            # TODO: Integrate with agent sau when refactor agent/
            # Hiện tại placeholder
            
            # Placeholder response
            response = f"[Agent response cho: {request.message}]"
            
            metadata = {
                "steps": 1,
                "tools_used": [],
                "provider": "placeholder"
            }
            
            return ChatResponse(
                response=response,
                conversation_id=conversation_id,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(
                f"Chat failed: {e}",
                exc_info=e,
                extra={"conversation_id": conversation_id}
            )
            raise AgentError(
                message="Failed to process chat request",
                details={
                    "conversation_id": conversation_id,
                    "error": str(e)
                }
            )
    
    async def list_tools(self) -> Dict[str, Any]:
        List all tools mà agent có thể dùng
        
        Returns:
            Dict with tools info
        # TODO: Get từ agent sau when refactor
        # Placeholder
        tools = [
            {
                "name": "add",
                "description": "Cộng hai số",
                "args": {"a": "float", "b": "float"}
            },
            {
                "name": "subtract",
                "description": "Trừ hai số",
                "args": {"a": "float", "b": "float"}
            },
            {
                "name": "multiply",
                "description": "Nhân hai số",
                "args": {"a": "float", "b": "float"}
            },
            {
                "name": "divide",
                "description": "Chia hai số",
                "args": {"a": "float", "b": "float"}
            }
        ]
        
        return {
            "total": len(tools),
            "tools": tools
        }
