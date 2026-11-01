Security Configuration
Học tập từ P-041: src/core/config/security.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class SecurityConfig(BaseSettings):
    Security-related configuration
    
    # JWT (cho future authentication)
    JWT_SECRET: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # API Keys (cho future API protection)
    API_KEY_ENABLED: bool = False
    API_KEY_HEADER: str = "X-API-Key"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Input Validation
    MAX_INPUT_LENGTH: int = 10000  # Max chars trong user input
    MAX_FILE_SIZE_MB: int = 10  # Max file upload size
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

# Singleton
_security_config: Optional[SecurityConfig] = None

def get_security_config() -> SecurityConfig:
    """Get security config singleton"""
    global _security_config
    if _security_config is None:
        _security_config = SecurityConfig()
    return _security_config
