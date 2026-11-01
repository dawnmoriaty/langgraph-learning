from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.agents.calculator_agent import run_agent
import uuid

router = APIRouter()


@router.get("/")
async def root():
    return {
        "status": "ok",
        "message": "LangGraph FastAPI Demo đang chạy! 🚀",
        "docs": "/docs"
    }


@router.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "langgraph-fastapi",
        "version": "0.1.0"
    }


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat với calculator agent
    
    Agent có thể:
    - Cộng, trừ, nhân, chia các số
    - Xử lý các phép tính phức tạp
    - Trả lời bằng tiếng Việt
    
    Example requests:
    - "Tính 25 * 4 + 10"
    - "15 chia cho 3 bằng bao nhiêu?"
    - "(100 - 20) * 2"
    """
    try:
        # Generate conversation ID nếu chưa có
        conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        
        # Run agent
        result = await run_agent(request.message)
        
        # Tạo metadata
        metadata = {
            "steps": result.get("steps", 0),
            "message_count": len(result.get("messages", []))
        }
        
        # Return response
        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id,
            metadata=metadata
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi xử lý: {str(e)}"
        )


@router.get("/tools")
async def list_tools():
    """
    Liệt kê tất cả tools mà agent có thể sử dụng
    """
    from app.agents.tools import ALL_TOOLS
    
    tools_info = []
    for tool in ALL_TOOLS:
        tools_info.append({
            "name": tool.name,
            "description": tool.description,
            "args": tool.args
        })
    
    return {
        "total": len(tools_info),
        "tools": tools_info
    }
