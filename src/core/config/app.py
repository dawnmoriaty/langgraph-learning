Application Configuration
Học tập từ P-041: src/core/config/app.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class AppConfig(BaseSettings):
    Application-level configuration
    
    # Application Identity
    APP_NAME: str = "LangGraph FastAPI Demo"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"  # development, production, test
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FORMAT: str = "json"  # json, text
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.APP_ENV == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.APP_ENV == "production"
    
    @property
    def is_test(self) -> bool:
        """Check if running tests"""
        return self.APP_ENV == "test"

# Singleton
_app_config: Optional[AppConfig] = None

def get_app_config() -> AppConfig:
    """Get application config singleton"""
    global _app_config
    if _app_config is None:
        _app_config = AppConfig()
    return _app_config
