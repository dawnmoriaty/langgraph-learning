Health module schemas
from pydantic import BaseModel, Field
from typing import Dict, Any, List

class HealthResponse(BaseModel):
    """Basic health response"""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="App version")
    environment: str = Field(..., description="Environment")

class ProviderHealth(BaseModel):
    provider: str
    status: str
    available: bool
    response_time: float | None = None
    error: str | None = None

class IntegrationsHealthResponse(BaseModel):
    """Integrations health response"""
    overall_status: str = Field(..., description="Overall status")
    total: int = Field(..., description="Total providers")
    healthy: int = Field(..., description="Healthy providers")
    providers: List[ProviderHealth] = Field(..., description="Provider details")
