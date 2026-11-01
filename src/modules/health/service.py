Health Service - Business logic cho health checks
from typing import Dict, Any
import time

from src.core.config import get_settings
from src.integrations import get_llm_registry, IntegrationHealthChecker

class HealthService:
    Service layer cho health checks
    
    Separation of concerns:
    - Router chỉ handle HTTP
    - Service chứa business logic
    - Repository (future) sẽ handle data access
    
    def __init__(self):
        self.settings = get_settings()
    
    def basic_health(self) -> Dict[str, Any]:
        Basic health check - chỉ check app đang chạy
        
        Returns:
            Dict với basic status
        return {
            "status": "healthy",
            "version": self.settings.app.APP_VERSION,
            "environment": self.settings.app.APP_ENV,
            "timestamp": time.time()
        }
    
    def detailed_health(self) -> Dict[str, Any]:
        Detailed health với system info
        
        Returns:
            Dict với detailed system info
        # Get config summary
        config_summary = self.settings.summary()
        
        # Add warnings nếu có
        warnings = self.settings.validate()
        
        return {
            "status": "healthy",
            "version": self.settings.app.APP_VERSION,
            "environment": self.settings.app.APP_ENV,
            "timestamp": time.time(),
            "config": config_summary,
            "warnings": warnings
        }
    
    async def check_integrations(self) -> Dict[str, Any]:
        Check health của LLM integrations
        
        Thực hiện LLM calls thật để test
        
        Returns:
            Dict với integration status
        try:
            registry = get_llm_registry()
            checker = IntegrationHealthChecker(timeout=10.0)
            
            # Run health check
            result = await checker.check_all()
            
            return result
            
        except RuntimeError as e:
            # Registry chưa được init
            return {
                "overall_status": "not_initialized",
                "error": str(e),
                "total": 0,
                "healthy": 0,
                "providers": []
            }
    
    async def readiness_check(self) -> Dict[str, Any]:
        Readiness check - system có sẵn sàng không?
        
        Checks:
        - Config đã load
        - Có ít nhất 1 LLM provider healthy
        
        Returns:
            Dict với readiness status
        checks = {
            "config_loaded": False,
            "llm_providers_available": False,
            "llm_providers_healthy": False
        }
        
        # Check 1: Config loaded
        try:
            _ = self.settings.app.APP_NAME
            checks["config_loaded"] = True
        except Exception:
            pass
        
        # Check 2: LLM providers
        try:
            registry = get_llm_registry()
            available = registry.list_available_providers()
            checks["llm_providers_available"] = len(available) > 0
            
            # Check 3: Quick health check
            if checks["llm_providers_available"]:
                health = await self.check_integrations()
                checks["llm_providers_healthy"] = health.get("healthy", 0) > 0
        except Exception:
            pass
        
        # Overall ready nếu tất cả checks pass
        ready = all(checks.values())
        
        return {
            "ready": ready,
            "checks": checks,
            "timestamp": time.time()
        }
