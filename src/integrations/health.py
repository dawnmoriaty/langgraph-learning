Integration Health Checker - Test API keys và connections
from typing import Dict, List, Any, Optional
from langchain_core.messages import HumanMessage
import asyncio
import logging
import time

from .llm_registry import get_llm_registry

logger = logging.getLogger(__name__)

class IntegrationHealthChecker:
    Health checker for integrations
    
    Usage:
        checker = IntegrationHealthChecker()
        results = await checker.check_all()
        
        # Check cụ thể
        result = await checker.check_provider("openai")
    
    def __init__(self, timeout: float = 5.0):
        Args:
            timeout: Timeout for each health check (seconds)
        self.timeout = timeout
    
    async def check_provider(
        self,
        provider_name: str
    ) -> Dict[str, Any]:
        Check health of một provider
        
        Args:
            provider_name: Tên provider
            
        Returns:
            Dict chứa status và thông tin
        registry = get_llm_registry()
        
        result = {
            "provider": provider_name,
            "status": "unknown",
            "available": False,
            "response_time": None,
            "error": None,
            "metadata": {}
        }
        
        try:
            # Get config
            config = registry.get_provider_config(provider_name)
            
            if not config:
                result["status"] = "not_registered"
                result["error"] = f"Provider '{provider_name}' chưa được đăng ký"
                return result
            
            # Check API key
            if not config.is_available():
                result["status"] = "no_api_key"
                result["error"] = f"API key for {config.provider.value} no"
                return result
            
            result["available"] = True
            result["metadata"] = {
                "provider_type": config.provider.value,
                "model": config.model
            }
            
            # Test with LLM call thật
            start_time = time.time()
            
            try:
                llm = config.create_llm()
                
                # Simple test call
                response = await asyncio.wait_for(
                    llm.ainvoke([HumanMessage(content="Hi")]),
                    timeout=self.timeout
                )
                
                response_time = time.time() - start_time
                result["response_time"] = round(response_time, 3)
                result["status"] = "healthy"
                
                # Extract metadata từ response
                if hasattr(response, "response_metadata"):
                    result["metadata"]["llm_response"] = response.response_metadata
                
                logger.info(
                    f" Provider '{provider_name}' healthy "
                    f"(response time: {response_time:.3f}s)"
                )
                
            except asyncio.TimeoutError:
                result["status"] = "timeout"
                result["error"] = f"Timeout sau {self.timeout}s"
                logger.warning(f"  Provider '{provider_name}' timeout")
                
            except Exception as e:
                result["status"] = "error"
                result["error"] = str(e)
                logger.error(f" Provider '{provider_name}' error: {e}")
        
        except Exception as e:
            result["status"] = "error"
            result["error"] = f"Unexpected error: {str(e)}"
            logger.error(f" Provider '{provider_name}' check failed: {e}")
        
        return result
    
    async def check_all(self) -> Dict[str, Any]:
        Check health of all providers
        
        Returns:
            Dict chứa tổng hợp kết quả
        registry = get_llm_registry()
        providers = [p["name"] for p in registry.list_providers()]
        
        logger.info(f" Checking {len(providers)} providers...")
        
        # Check song song
        tasks = [self.check_provider(name) for name in providers]
        results = await asyncio.gather(*tasks)
        
        # Tổng hợp
        summary = {
            "total": len(results),
            "healthy": sum(1 for r in results if r["status"] == "healthy"),
            "available": sum(1 for r in results if r["available"]),
            "providers": results,
            "timestamp": time.time()
        }
        
        # Overall status
        if summary["healthy"] > 0:
            summary["overall_status"] = "healthy"
        elif summary["available"] > 0:
            summary["overall_status"] = "degraded"
        else:
            summary["overall_status"] = "unhealthy"
        
        logger.info(
            f" Health check complete: "
            f"{summary['healthy']}/{summary['total']} healthy"
        )
        
        return summary
    
    async def test_fallback(
        self,
        preferred_order: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        Test fallback mechanism
        
        Args:
            preferred_order: Thứ tự ưu tiên providers
            
        Returns:
            Dict chứa kết quả test
        registry = get_llm_registry()
        
        result = {
            "requested_order": preferred_order or "auto",
            "selected_provider": None,
            "status": "unknown",
            "response_time": None,
            "error": None
        }
        
        try:
            start_time = time.time()
            
            # Get LLM with fallback
            llm = registry.get_llm_with_fallback(preferred_order)
            
            # Test call
            response = await asyncio.wait_for(
                llm.ainvoke([HumanMessage(content="Test")]),
                timeout=self.timeout
            )
            
            response_time = time.time() - start_time
            result["response_time"] = round(response_time, 3)
            result["status"] = "success"
            
            # Detect provider từ response
            if hasattr(response, "response_metadata"):
                metadata = response.response_metadata
                if "model_name" in metadata:
                    result["selected_provider"] = metadata["model_name"]
            
            logger.info(f" Fallback test successful (time: {response_time:.3f}s)")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.error(f" Fallback test failed: {e}")
        
        return result

# Convenience functions

async def quick_health_check() -> bool:
    Quick health check - return True if có ít nhất 1 provider healthy
    
    Returns:
        True if có provider healthy, False if không
    try:
        checker = IntegrationHealthChecker(timeout=3.0)
        results = await checker.check_all()
        return results["healthy"] > 0
    except Exception as e:
        logger.error(f"Quick health check failed: {e}")
        return False

async def get_health_summary() -> Dict[str, Any]:
    Get health summary of all providers
    
    Returns:
        Dict chứa health status
    checker = IntegrationHealthChecker()
    return await checker.check_all()
