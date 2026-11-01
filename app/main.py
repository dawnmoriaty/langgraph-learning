"""
Main FastAPI Application
Entry point của ứng dụng
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings

# Tạo FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    🤖 **LangGraph với FastAPI Demo**
    
    Đây là một ứng dụng demo về cách tích hợp LangGraph với FastAPI.
    
    ## Features
    
    - ✅ Calculator Agent với 4 tools (cộng, trừ, nhân, chia)
    - ✅ LangGraph workflow với StateGraph
    - ✅ RESTful API với FastAPI
    - ✅ Hỗ trợ cả OpenAI và Anthropic
    - ✅ Type-safe với Pydantic models
    
    ## Cách sử dụng
    
    1. Gọi POST `/chat` với message của bạn
    2. Agent sẽ tự động quyết định có cần dùng tools không
    3. Nhận kết quả và metadata về quá trình xử lý
    
    ## Example
    
    ```bash
    curl -X POST "http://localhost:8000/chat" \\
         -H "Content-Type: application/json" \\
         -d '{"message": "Tính 25 * 4 + 10"}'
    ```
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên specify cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, tags=["LangGraph Agent"])


@app.on_event("startup")
async def startup_event():
    """Chạy khi app khởi động"""
    print("\n" + "="*60)
    print(f"🚀 {settings.APP_NAME} đang khởi động...")
    print("="*60)
    print(f"📍 Host: {settings.HOST}:{settings.PORT}")
    print(f"📚 Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    
    # Check API keys
    if settings.OPENAI_API_KEY:
        print("✅ OpenAI API key detected")
    if settings.ANTHROPIC_API_KEY:
        print("✅ Anthropic API key detected")
    
    if not settings.OPENAI_API_KEY and not settings.ANTHROPIC_API_KEY:
        print("⚠️  WARNING: Không tìm thấy API key!")
        print("   Hãy set OPENAI_API_KEY hoặc ANTHROPIC_API_KEY trong .env")
    
    print("="*60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Chạy khi app tắt"""
    print("\n👋 Đang tắt server...")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
