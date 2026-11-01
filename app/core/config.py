from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Settings class để load config từ .env file"""
    
    # Application
    APP_NAME: str = "LangGraph FastAPI Demo"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API Keys - Chỉ cần một trong những key này
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # LangSmith (optional - để trace và debug)
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "langgraph-demo"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton instance
settings = Settings()
