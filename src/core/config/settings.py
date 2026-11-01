Settings - Tổng hợp tất cả configs
from typing import Optional
from .app import AppConfig, get_app_config
from .llm import LLMConfig, get_llm_config
from .agent import AgentConfig, get_agent_config
from .security import SecurityConfig, get_security_config

class Settings:
    Unified settings object chứa tất cả configs
    
    Usage:
        from src.core.config import get_settings
        
        settings = get_settings()
        print(settings.app.APP_NAME)
        print(settings.llm.OPENAI_API_KEY)
        print(settings.agent.AGENT_MAX_STEPS)
        print(settings.security.JWT_SECRET)
    
    def __init__(self):
        self._app: Optional[AppConfig] = None
        self._llm: Optional[LLMConfig] = None
        self._agent: Optional[AgentConfig] = None
        self._security: Optional[SecurityConfig] = None
    
    @property
    def app(self) -> AppConfig:
        """Application config"""
        if self._app is None:
            self._app = get_app_config()
        return self._app
    
    @property
    def llm(self) -> LLMConfig:
        """LLM config"""
        if self._llm is None:
            self._llm = get_llm_config()
        return self._llm
    
    @property
    def agent(self) -> AgentConfig:
        """Agent config"""
        if self._agent is None:
            self._agent = get_agent_config()
        return self._agent
    
    @property
    def security(self) -> SecurityConfig:
        """Security config"""
        if self._security is None:
            self._security = get_security_config()
        return self._security
    
    def validate(self) -> list[str]:
        Validate all configs và return danh sách warnings
        
        Returns:
            List of warning messages
        warnings = []
        
        # Check LLM keys
        if not self.llm.has_any_key:
            warnings.append(
                "  Không có LLM API key! Set OPENAI_API_KEY, "
                "ANTHROPIC_API_KEY, hoặc GOOGLE_API_KEY"
            )
        
        # Check JWT secret in production
        if self.app.is_production and not self.security.JWT_SECRET:
            warnings.append(
                "  JWT_SECRET không được set trong production!"
            )
        
        # Check debug in production
        if self.app.is_production and self.app.DEBUG:
            warnings.append(
                "  DEBUG=True trong production! Nên set DEBUG=False"
            )
        
        return warnings
    
    def summary(self) -> dict:
        return {
            "app": {
                "name": self.app.APP_NAME,
                "version": self.app.APP_VERSION,
                "env": self.app.APP_ENV,
                "debug": self.app.DEBUG,
                "host": self.app.HOST,
                "port": self.app.PORT,
            },
            "llm": {
                "available_providers": self.llm.available_providers,
                "temperature": self.llm.LLM_TEMPERATURE,
                "max_tokens": self.llm.LLM_MAX_TOKENS,
                "timeout": self.llm.LLM_TIMEOUT_SECONDS,
            },
            "agent": {
                "max_steps": self.agent.AGENT_MAX_STEPS,
                "max_tool_calls": self.agent.AGENT_MAX_TOOL_CALLS,
                "input_guard": self.agent.INPUT_GUARD_ENABLED,
                "output_guard": self.agent.OUTPUT_GUARD_ENABLED,
            },
            "security": {
                "jwt_configured": bool(self.security.JWT_SECRET),
                "api_key_enabled": self.security.API_KEY_ENABLED,
                "rate_limit_enabled": self.security.RATE_LIMIT_ENABLED,
            }
        }

# Singleton
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get unified settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
