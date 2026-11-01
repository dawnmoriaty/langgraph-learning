"""LLM Provider Registry with automatic fallback."""
from typing import Optional, List, Dict, Any
from enum import Enum
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseChatModel
import logging

logger = logging.getLogger(__name__)

class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"

class ProviderConfig:
    
    def __init__(
        self,
        provider: LLMProvider,
        api_key: Optional[str],
        model: str,
        temperature: float = 0.0,
        max_tokens: int = 4096,
        **kwargs
    ):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kwargs = kwargs
    
    def is_available(self) -> bool:
        """Check if provider has API key"""
        return bool(self.api_key)
    
    def create_llm(self) -> BaseChatModel:
        """Create LLM instance"""
        if not self.is_available():
            raise ValueError(f"API key for {self.provider} not found")
        
        common_params = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        
        if self.provider == LLMProvider.OPENAI:
            return ChatOpenAI(
                model=self.model,
                api_key=self.api_key,
                **common_params,
                **self.kwargs
            )
        elif self.provider == LLMProvider.ANTHROPIC:
            return ChatAnthropic(
                model=self.model,
                api_key=self.api_key,
                **common_params,
                **self.kwargs
            )
        elif self.provider == LLMProvider.GOOGLE:
            return ChatGoogleGenerativeAI(
                model=self.model,
                google_api_key=self.api_key,
                **common_params,
                **self.kwargs
            )
        else:
            raise ValueError(f"Provider không hỗ trợ: {self.provider}")

class LLMRegistry:
    """Registry managing multiple LLM providers with automatic fallback."""
    
    def __init__(self):
        self._providers: Dict[str, ProviderConfig] = {}
        self._primary: Optional[str] = None
    
    def register(
        self,
        name: str,
        config: ProviderConfig,
        primary: bool = False
    ) -> None:
        """Register a provider."""
        self._providers[name] = config
        
        if primary or self._primary is None:
            self._primary = name
        
        logger.info(
            f"Registered provider '{name}' ({config.provider.value}) - "
            f"Available: {config.is_available()}"
        )
    
    def get_provider_config(self, name: str) -> Optional[ProviderConfig]:
        """Get provider configuration."""
        return self._providers.get(name)
    
    def list_providers(self) -> List[Dict[str, Any]]:
        """List all registered providers."""
        return [
            {
                "name": name,
                "provider": config.provider.value,
                "model": config.model,
                "available": config.is_available(),
                "is_primary": name == self._primary
            }
            for name, config in self._providers.items()
        ]
    
    def list_available_providers(self) -> List[str]:
        """Liệt kê providers có API key"""
        return [
            name
            for name, config in self._providers.items()
            if config.is_available()
        ]
    
    def get_llm(self, name: Optional[str] = None) -> BaseChatModel:
        Lấy LLM instance
        
        Args:
            name: Tên provider (None = dùng primary)
            
        Returns:
            LLM instance
            
        Raises:
            ValueError: Nếu provider không tồn tại hoặc không available
        target_name = name or self._primary
        
        if not target_name:
            raise ValueError("Không có provider nào được đăng ký!")
        
        config = self._providers.get(target_name)
        if not config:
            raise ValueError(f"Provider '{target_name}' không tồn tại!")
        
        if not config.is_available():
            raise ValueError(
                f"Provider '{target_name}' không có API key! "
                f"Hãy set {config.provider.value.upper()}_API_KEY"
            )
        
        logger.info(f"Creating LLM instance: {target_name} ({config.model})")
        return config.create_llm()
    
    def get_llm_with_fallback(
        self,
        preferred_order: Optional[List[str]] = None
    ) -> BaseChatModel:
        Lấy LLM với automatic fallback
        
        Args:
            preferred_order: Thứ tự ưu tiên (None = dùng primary rồi bất kỳ)
            
        Returns:
            LLM instance đầu tiên available
            
        Raises:
            ValueError: Nếu không có provider nào available
        # Nếu không có preferred order, dùng primary rồi tất cả
        if preferred_order is None:
            if self._primary:
                preferred_order = [self._primary]
            else:
                preferred_order = []
            
            # Thêm tất cả providers khác
            preferred_order.extend([
                name for name in self._providers.keys()
                if name not in preferred_order
            ])
        
        # Thử từng provider theo thứ tự
        for name in preferred_order:
            config = self._providers.get(name)
            
            if config and config.is_available():
                logger.info(
                    f" Using provider: {name} ({config.provider.value})"
                )
                return config.create_llm()
            elif config:
                logger.warning(
                    f"  Provider '{name}' không có API key, skip..."
                )
            else:
                logger.warning(
                    f"  Provider '{name}' không tồn tại, skip..."
                )
        
        # Không có provider nào available
        available = self.list_available_providers()
        if available:
            # Có providers nhưng không trong preferred list
            logger.warning(
                f"Không có provider nào trong preferred list available. "
                f"Dùng provider đầu tiên: {available[0]}"
            )
            return self.get_llm(available[0])
        else:
            raise ValueError(
                "Không có provider nào available! "
                "Hãy set ít nhất một API key: "
                "OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY"
            )

# Singleton instance
_registry: Optional[LLMRegistry] = None

def get_llm_registry() -> LLMRegistry:
    """Get global LLM registry instance"""
    global _registry
    
    if _registry is None:
        raise RuntimeError(
            "LLM Registry chưa được khởi tạo! "
            "Hãy gọi initialize_llm_registry() trước."
        )
    
    return _registry

def initialize_llm_registry(
    openai_key: Optional[str] = None,
    anthropic_key: Optional[str] = None,
    google_key: Optional[str] = None,
    default_temperature: float = 0.0,
    default_max_tokens: int = 4096
) -> LLMRegistry:
    Khởi tạo global LLM registry
    
    Args:
        openai_key: OpenAI API key
        anthropic_key: Anthropic API key
        google_key: Google API key
        default_temperature: Temperature mặc định
        default_max_tokens: Max tokens mặc định
        
    Returns:
        LLM Registry instance
    global _registry
    
    _registry = LLMRegistry()
    
    # Register OpenAI
    if openai_key:
        _registry.register(
            "openai",
            ProviderConfig(
                provider=LLMProvider.OPENAI,
                api_key=openai_key,
                model="gpt-4o-mini",
                temperature=default_temperature,
                max_tokens=default_max_tokens
            ),
            primary=True
        )
    
    # Register Anthropic
    if anthropic_key:
        _registry.register(
            "anthropic",
            ProviderConfig(
                provider=LLMProvider.ANTHROPIC,
                api_key=anthropic_key,
                model="claude-3-5-sonnet-20241022",
                temperature=default_temperature,
                max_tokens=default_max_tokens
            ),
            primary=not openai_key  # Primary nếu OpenAI không có
        )
    
    # Register Google
    if google_key:
        _registry.register(
            "google",
            ProviderConfig(
                provider=LLMProvider.GOOGLE,
                api_key=google_key,
                model="gemini-1.5-flash",
                temperature=default_temperature,
                max_tokens=default_max_tokens
            ),
            primary=not (openai_key or anthropic_key)
        )
    
    available = _registry.list_available_providers()
    logger.info(
        f" LLM Registry initialized with {len(available)} providers: "
        f"{', '.join(available)}"
    )
    
    return _registry
