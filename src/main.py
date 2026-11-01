"""Main FastAPI Application - Refactored Structure."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.core.config import get_settings
from src.core.common import register_exception_handlers
from src.integrations import initialize_llm_registry
from src.modules.health import router as health_router
from src.modules.chat import router as chat_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for app startup and shutdown."""
    logger.info("=" * 60)
    logger.info("Starting application...")
    logger.info("=" * 60)
    
    settings = get_settings()
    
    logger.info(f"App: {settings.app.APP_NAME} v{settings.app.APP_VERSION}")
    logger.info(f"Environment: {settings.app.APP_ENV}")
    logger.info(f"Host: {settings.app.HOST}:{settings.app.PORT}")
    logger.info(f"Debug: {settings.app.DEBUG}")
    
    logger.info("\nInitializing LLM Registry...")
    try:
        registry = initialize_llm_registry(
            openai_key=settings.llm.OPENAI_API_KEY,
            anthropic_key=settings.llm.ANTHROPIC_API_KEY,
            google_key=settings.llm.GOOGLE_API_KEY,
            default_temperature=settings.llm.LLM_TEMPERATURE,
            default_max_tokens=settings.llm.LLM_MAX_TOKENS
        )
        
        available = registry.list_available_providers()
        logger.info(f"{len(available)} providers available: {', '.join(available)}")
        
    except Exception as e:
        logger.warning(f"LLM Registry initialization failed: {e}")
    
    warnings = settings.validate()
    if warnings:
        logger.warning("\nConfiguration warnings:")
        for warning in warnings:
            logger.warning(f"  {warning}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Application started successfully!")
    logger.info("=" * 60)
    logger.info(f"Docs: http://{settings.app.HOST}:{settings.app.PORT}/docs")
    logger.info(f"Health: http://{settings.app.HOST}:{settings.app.PORT}/health")
    logger.info("=" * 60 + "\n")
    
    yield
    
    logger.info("\nShutting down application...")


settings = get_settings()

app = FastAPI(
    title=settings.app.APP_NAME,
    version=settings.app.APP_VERSION,
    description="""
    LangGraph with FastAPI Demo - Refactored
    
    Features:
    - Provider registry with automatic fallback
    - Config management by domain
    - Envelope response pattern
    - Structured error handling
    - Router to Service separation
    - Integration health checks
    
    ## API Endpoints
    
    - Calculator Agent with 4 tools
    - Multi-provider LLM support (OpenAI, Anthropic, Google)
    - Automatic fallback
    - Health checks with LLM tests
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app.CORS_ORIGINS,
    allow_credentials=settings.app.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.app.CORS_ALLOW_METHODS,
    allow_headers=settings.app.CORS_ALLOW_HEADERS,
)

register_exception_handlers(app)

app.include_router(health_router)
app.include_router(chat_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"{settings.app.APP_NAME} is running!",
        "version": settings.app.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.app.HOST,
        port=settings.app.PORT,
        reload=settings.app.DEBUG
    )
