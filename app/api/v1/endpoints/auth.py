from fastapi import APIRouter, HTTPException, status, Depends
from app.models.auth import UserCreate, UserLogin, User, Token
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user
import logging
import traceback

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        user = await AuthService.register_user(user_data)
        logger.info(f"✅ User registered successfully: {user_data.email}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"❌ Registration failed for {user_data.email}: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and return access token"""
    try:
        token = await AuthService.login(user_credentials)
        logger.info(f"✅ User logged in successfully: {user_credentials.email}")
        return token
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"❌ Login failed for {user_credentials.email}: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user
