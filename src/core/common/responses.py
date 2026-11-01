API Response Envelope Pattern
Học tập từ P-041: src/core/common/responses.py

Tất cả API responses đi qua envelope pattern:
{
    "success": true,
    "data": {...},
    "error": null,
    "meta": {...}
}
from typing import Any, Optional, Dict, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class ErrorDetail(BaseModel):
    """Error details"""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")

class APIResponse(BaseModel, Generic[T]):
    Standard API response envelope
    
    Examples:
        Success:
        {
            "success": true,
            "data": {"id": 1, "name": "Test"},
            "error": null,
            "meta": {"timestamp": 1234567890}
        }
        
        Error:
        {
            "success": false,
            "data": null,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input",
                "details": {"field": "email"}
            },
            "meta": null
        }
    success: bool = Field(..., description="Request success status")
    data: Optional[T] = Field(None, description="Response data")
    error: Optional[ErrorDetail] = Field(None, description="Error details nếu failed")
    meta: Optional[Dict[str, Any]] = Field(None, description="Metadata (pagination, etc)")
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "success": True,
                    "data": {"message": "Operation successful"},
                    "error": None,
                    "meta": {"timestamp": 1234567890}
                }
            ]
        }

def success_response(
    data: Any = None,
    meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    Tạo success response
    
    Args:
        data: Response data
        meta: Optional metadata
        
    Returns:
        Dict với envelope format
        
    Examples:
        >>> success_response({"id": 1})
        {"success": True, "data": {"id": 1}, "error": None, "meta": None}
        
        >>> success_response(
        ...     data=[{"id": 1}, {"id": 2}],
        ...     meta={"total": 2, "page": 1}
        ... )
    return {
        "success": True,
        "data": data,
        "error": None,
        "meta": meta
    }

def error_response(
    code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    Tạo error response
    
    Args:
        code: Error code (e.g., "VALIDATION_ERROR")
        message: Human-readable error message
        details: Optional additional details
        meta: Optional metadata
        
    Returns:
        Dict với envelope format
        
    Examples:
        >>> error_response(
        ...     code="NOT_FOUND",
        ...     message="User not found",
        ...     details={"user_id": 123}
        ... )
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details
        },
        "meta": meta
    }

class PaginatedResponse(BaseModel, Generic[T]):
    Response với pagination
    
    Examples:
        {
            "success": true,
            "data": [{"id": 1}, {"id": 2}],
            "error": null,
            "meta": {
                "total": 100,
                "page": 1,
                "limit": 20,
                "pages": 5,
                "has_next": true,
                "has_prev": false
            }
        }
    success: bool = True
    data: list[T] = Field(default_factory=list)
    error: Optional[ErrorDetail] = None
    meta: Dict[str, Any] = Field(
        ...,
        description="Pagination metadata"
    )

def paginated_response(
    items: list[Any],
    total: int,
    page: int = 1,
    limit: int = 20,
    **extra_meta
) -> Dict[str, Any]:
    Tạo paginated response
    
    Args:
        items: List items cho page hiện tại
        total: Tổng số items
        page: Current page number (1-indexed)
        limit: Items per page
        **extra_meta: Additional metadata
        
    Returns:
        Dict với pagination envelope
        
    Examples:
        >>> items = [{"id": 1}, {"id": 2}]
        >>> paginated_response(items, total=100, page=1, limit=20)
    pages = (total + limit - 1) // limit  # Ceiling division
    
    meta = {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1,
        **extra_meta
    }
    
    return {
        "success": True,
        "data": items,
        "error": None,
        "meta": meta
    }
