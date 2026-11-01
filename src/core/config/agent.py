Agent Configuration
Học tập từ P-041: src/core/config/agent.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class AgentConfig(BaseSettings):
    LangGraph agent configuration
    
    # Agent Behavior
    AGENT_MAX_STEPS: int = 10  # Max iterations in agent loop
    AGENT_MAX_TOOL_CALLS: int = 5  # Max tool calls in 1 turn
    AGENT_TIMEOUT_SECONDS: int = 60  # Timeout for entire agent execution
    
    # Tool Settings
    TOOL_TIMEOUT_SECONDS: int = 10  # Timeout for each tool call
    TOOL_MAX_RETRIES: int = 2  # Retry when tool fails
    
    # Guardrails
    INPUT_GUARD_ENABLED: bool = True  # Enable input validation
    OUTPUT_GUARD_ENABLED: bool = True  # Enable output validation
    
    # Memory
    AGENT_MEMORY_ENABLED: bool = False  # Enable conversation memory
    AGENT_MAX_MEMORY_MESSAGES: int = 10  # Max messages to keep in memory
    
    # Streaming
    AGENT_STREAMING_ENABLED: bool = False  # Enable streaming responses
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

# Singleton
_agent_config: Optional[AgentConfig] = None

def get_agent_config() -> AgentConfig:
    """Get agent config singleton"""
    global _agent_config
    if _agent_config is None:
        _agent_config = AgentConfig()
    return _agent_config
