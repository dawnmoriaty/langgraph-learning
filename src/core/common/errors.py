Structured Error Classes
Học tập từ P-041: src/core/common/errors.py

Hierarchy:
    AppError (base)
    ├── ValidationError (400)
    ├── UnauthorizedError (401)
    ├── ForbiddenError (403)
    ├── NotFoundError (404)
    ├── ConflictError (409)
    └── InternalServerError (500)
from typing import Optional, Dict, Any

class AppError(Exception):
    Base application error
    
    Attributes:
        code: Error code (e.g., "VALIDATION_ERROR")
        message: Human-readable message
        status_code: HTTP status code
        details: Optional additional details
    
    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dict format"""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details
        }

class ValidationError(AppError):
    Validation error - 400 Bad Request
    
    Use when: User input không hợp lệ
    
    Examples:
        raise ValidationError("Email không hợp lệ")
        raise ValidationError(
            "Validation failed",
            details={"field": "email", "error": "Invalid format"}
        )
    
    def __init__(
        self,
        message: str = "Validation failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details
        )

class UnauthorizedError(AppError):
    Unauthorized error - 401
    
    Use when: User chưa đăng nhập hoặc token invalid
    
    Examples:
        raise UnauthorizedError("Token expired")
        raise UnauthorizedError("Missing authentication")
    
    def __init__(
        self,
        message: str = "Unauthorized",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
            details=details
        )

class ForbiddenError(AppError):
    Forbidden error - 403
    
    Use when: User authenticated nhưng không có permission
    
    Examples:
        raise ForbiddenError("Bạn không có quyền xóa user này")
        raise ForbiddenError("Admin only")
    
    def __init__(
        self,
        message: str = "Forbidden",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403,
            details=details
        )

class NotFoundError(AppError):
    Not found error - 404
    
    Use when: Resource không tồn tại
    
    Examples:
        raise NotFoundError("User not found")
        raise NotFoundError(
            "User not found",
            details={"user_id": 123}
        )
    
    def __init__(
        self,
        message: str = "Resource not found",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details=details
        )

class ConflictError(AppError):
    Conflict error - 409
    
    Use when: Resource đã tồn tại hoặc có conflict
    
    Examples:
        raise ConflictError("Email already exists")
        raise ConflictError(
            "Cannot delete user with active orders",
            details={"user_id": 123, "active_orders": 5}
        )
    
    def __init__(
        self,
        message: str = "Conflict",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409,
            details=details
        )

class InternalServerError(AppError):
    Internal server error - 500
    
    Use when: Lỗi không mong đợi
    
    Examples:
        raise InternalServerError("Database connection failed")
        raise InternalServerError(
            "LLM provider error",
            details={"provider": "openai", "error": "timeout"}
        )
    
    def __init__(
        self,
        message: str = "Internal server error",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="INTERNAL_ERROR",
            status_code=500,
            details=details
        )

class AgentError(AppError):
    Agent execution error
    
    Use when: Agent fails trong quá trình execution
    
    Examples:
        raise AgentError("Agent timeout")
        raise AgentError(
            "Max iterations exceeded",
            details={"max_steps": 10, "current_step": 11}
        )
    
    def __init__(
        self,
        message: str = "Agent execution failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="AGENT_ERROR",
            status_code=500,
            details=details
        )

class LLMError(AppError):
    LLM provider error
    
    Use when: LLM call fails
    
    Examples:
        raise LLMError("All providers failed")
        raise LLMError(
            "OpenAI timeout",
            details={"provider": "openai", "timeout": 30}
        )
    
    def __init__(
        self,
        message: str = "LLM provider error",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="LLM_ERROR",
            status_code=500,
            details=details
        )
