from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import init_db, close_db

logging.basicConfig(level=logging.INFO)
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
