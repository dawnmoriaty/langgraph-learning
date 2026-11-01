LLM Configuration
Học tập từ P-041: src/core/config/llm.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class LLMConfig(BaseSettings):
    LLM provider configuration
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # LLM Settings
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 4096
    LLM_TIMEOUT_SECONDS: int = 30
    LLM_MAX_RETRIES: int = 3
    
    # Provider Preferences
    LLM_PRIMARY_PROVIDER: Optional[str] = None  # openai, anthropic, google
    LLM_FALLBACK_ORDER: str = "openai,anthropic,google"  # Comma-separated
    
    # Models
    OPENAI_MODEL: str = "gpt-4o-mini"
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    GOOGLE_MODEL: str = "gemini-1.5-flash"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def has_any_key(self) -> bool:
        """Check if có ít nhất 1 API key"""
        return bool(
            self.OPENAI_API_KEY or 
            self.ANTHROPIC_API_KEY or 
            self.GOOGLE_API_KEY
        )
    
    @property
    def available_providers(self) -> list[str]:
        """List các providers có API key"""
        providers = []
        if self.OPENAI_API_KEY:
            providers.append("openai")
        if self.ANTHROPIC_API_KEY:
            providers.append("anthropic")
        if self.GOOGLE_API_KEY:
            providers.append("google")
        return providers
    
    def get_fallback_order(self) -> list[str]:
        """Parse fallback order từ string"""
        return [p.strip() for p in self.LLM_FALLBACK_ORDER.split(",") if p.strip()]

# Singleton
_llm_config: Optional[LLMConfig] = None

def get_llm_config() -> LLMConfig:
    """Get LLM config singleton"""
    global _llm_config
    if _llm_config is None:
        _llm_config = LLMConfig()
    return _llm_config
