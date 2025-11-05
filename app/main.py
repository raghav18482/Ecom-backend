from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
import sys
from datetime import datetime
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import init_db, close_db

# Configure logging with detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A complete FastAPI backend for an e-commerce hoodie store",
)

logger.info(f"CORS allowed origins: {settings.ALLOWED_ORIGINS}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses"""
    start_time = datetime.now()
    
    # Log request
    logger.info(
        f"📥 {request.method} {request.url.path} - "
        f"Client: {request.client.host if request.client else 'unknown'}"
    )
    
    try:
        response = await call_next(request)
        process_time = (datetime.now() - start_time).total_seconds()
        
        # Log response
        logger.info(
            f"📤 {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        
        return response
    except Exception as e:
        process_time = (datetime.now() - start_time).total_seconds()
        logger.error(
            f"❌ {request.method} {request.url.path} - "
            f"Error after {process_time:.3f}s: {str(e)}"
        )
        raise

# Global exception handler for 500 errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions and log them with full details"""
    error_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    # Get full traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    full_traceback = "".join(tb_lines)
    
    # Log detailed error information
    logger.error(
        f"\n{'='*80}\n"
        f"🚨 INTERNAL SERVER ERROR [{error_id}]\n"
        f"{'='*80}\n"
        f"Timestamp: {datetime.now().isoformat()}\n"
        f"Method: {request.method}\n"
        f"Path: {request.url.path}\n"
        f"Query Params: {dict(request.query_params)}\n"
        f"Client: {request.client.host if request.client else 'unknown'}\n"
        f"Error Type: {type(exc).__name__}\n"
        f"Error Message: {str(exc)}\n"
        f"{'-'*80}\n"
        f"Full Traceback:\n{full_traceback}\n"
        f"{'='*80}\n"
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "error_id": error_id,
            "message": "An unexpected error occurred. Please contact support with the error_id.",
            "timestamp": datetime.now().isoformat()
        }
    )

# Handler for validation errors (400)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Log validation errors"""
    logger.warning(
        f"⚠️  Validation Error: {request.method} {request.url.path} - {exc.errors()}"
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

# Handler for HTTP exceptions (400, 401, 404, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Log HTTP exceptions"""
    if exc.status_code >= 500:
        logger.error(
            f"❌ HTTP {exc.status_code}: {request.method} {request.url.path} - {exc.detail}"
        )
    else:
        logger.warning(
            f"⚠️  HTTP {exc.status_code}: {request.method} {request.url.path} - {exc.detail}"
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
    except Exception as e:
        logger.error(f"Database init failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

@app.get("/")
async def root():
    return {"message": "Welcome to Hoodie Store API", "version": settings.APP_VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
