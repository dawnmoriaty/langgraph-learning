FastAPI Exception Handlers
Convert exceptions sang API response envelope
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Union
import logging

from .errors import AppError
from .responses import error_response

logger = logging.getLogger(__name__)

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    Handler cho AppError và subclasses
    
    Convert AppError sang API response envelope
    logger.warning(
        f"AppError: {exc.code} - {exc.message}",
        extra={
            "code": exc.code,
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            code=exc.code,
            message=exc.message,
            details=exc.details
        )
    )

async def validation_error_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    Handler cho Pydantic validation errors
    
    Convert validation errors sang readable format
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        f"Validation error: {len(errors)} fields",
        extra={
            "errors": errors,
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details={"errors": errors}
        )
    )

async def generic_error_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    Handler cho tất cả exceptions khác
    
    Catch-all handler cho unexpected errors
    logger.error(
        f"Unhandled exception: {type(exc).__name__} - {str(exc)}",
        exc_info=exc,
        extra={"path": request.url.path}
    )
    
    # Trong development, show chi tiết error
    # Trong production, hide internal details
    from src.core.config import get_app_config
    config = get_app_config()
    
    if config.DEBUG:
        details = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": None  # Could add traceback in debug mode
        }
    else:
        details = None
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            details=details
        )
    )

def register_exception_handlers(app) -> None:
    Register tất cả exception handlers vào FastAPI app
    
    Usage:
        from fastapi import FastAPI
        from src.core.common.exception_handlers import register_exception_handlers
        
        app = FastAPI()
        register_exception_handlers(app)
    # AppError và subclasses
    app.add_exception_handler(AppError, app_error_handler)
    
    # Pydantic validation errors
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    
    # Generic exception handler (catch-all)
    app.add_exception_handler(Exception, generic_error_handler)
    
    logger.info(" Exception handlers registered")
