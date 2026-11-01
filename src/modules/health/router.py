Health Check Router
Endpoints để check system health và integrations
from fastapi import APIRouter, Depends
from typing import Dict, Any

from src.core.common import success_response
from .service import HealthService
from .schemas import HealthResponse, IntegrationsHealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

def get_health_service() -> HealthService:
    return HealthService()

@router.get("", response_model=Dict[str, Any])
async def health_check(
    service: HealthService = Depends(get_health_service)
) -> Dict[str, Any]:
    Basic health check
    
    Returns:
        200: System is running
    result = service.basic_health()
    return success_response(data=result)

@router.get("/detailed", response_model=Dict[str, Any])
async def detailed_health(
    service: HealthService = Depends(get_health_service)
) -> Dict[str, Any]:
    Detailed health check with system info
    
    Returns:
        System status và configurations
    result = service.detailed_health()
    return success_response(data=result)

@router.get("/integrations", response_model=Dict[str, Any])
async def integrations_health(
    service: HealthService = Depends(get_health_service)
) -> Dict[str, Any]:
    Check health of LLM integrations
    
    Execute LLM calls thật để test API keys
    
    Returns:
        Status of each LLM provider
    result = await service.check_integrations()
    return success_response(data=result)

@router.get("/ready", response_model=Dict[str, Any])
async def readiness_check(
    service: HealthService = Depends(get_health_service)
) -> Dict[str, Any]:
    Readiness check - System có sẵn sàng serve requests không?
    
    Returns:
        200 if ready, 503 if not ready
    result = await service.readiness_check()
    
    # Nếu not ready, return 503
    if not result.get("ready", False):
        from fastapi import status, HTTPException
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=result
        )
    
    return success_response(data=result)
