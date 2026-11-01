"""Script to run server."""
import uvicorn
from src.core.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print(f"""
Starting LangGraph FastAPI Demo Server (Refactored)

Server: http://{settings.app.HOST}:{settings.app.PORT}
Docs: http://{settings.app.HOST}:{settings.app.PORT}/docs
Health: http://{settings.app.HOST}:{settings.app.PORT}/health

Press CTRL+C to stop
""")
    
    uvicorn.run(
        "src.main:app",
        host=settings.app.HOST,
        port=settings.app.PORT,
        reload=settings.app.DEBUG,
        log_level="info"
    )
