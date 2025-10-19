from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from app.core.database import db
from app.core.config import settings
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.auth import UserCreate, UserLogin, User, Token
import uuid

class AuthService:
    @staticmethod
    async def register_user(user_data: UserCreate) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = await db.fetch_one(
            "SELECT id FROM auth.users WHERE email = $1", user_data.email
        )
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user (in a real app, this would integrate with Supabase Auth)
        user_id = str(uuid.uuid4())
        await db.execute(
            """
            INSERT INTO auth.users (id, email, encrypted_password, created_at, updated_at)
            VALUES ($1, $2, $3, NOW(), NOW())
            """,
            user_id, user_data.email, hashed_password
        )
        
        # Create profile
        await db.execute(
            """
            INSERT INTO profiles (id, user_id, full_name, created_at)
            VALUES ($1, $2, $3, NOW())
            """,
            user_id, user_id, user_data.full_name
        )
        
        return User(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            created_at=datetime.utcnow()
        )
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = await db.fetch_one(
            "SELECT id, email, encrypted_password, created_at FROM auth.users WHERE email = $1",
            email
        )
        
        if not user or not verify_password(password, user["encrypted_password"]):
            return None
        
        return User(
            id=str(user["id"]),  # Convert UUID to string
            email=user["email"],
            full_name=None,  # Will be fetched from profiles table
            created_at=user["created_at"].replace(tzinfo=None)  # Remove timezone info
        )
    
    @staticmethod
    async def login(user_credentials: UserLogin) -> Token:
        """Login user and return access token"""
        user = await AuthService.authenticate_user(user_credentials.email, user_credentials.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    @staticmethod
    async def get_current_user(user_id: str) -> Optional[User]:
        """Get current user by ID"""
        user = await db.fetch_one(
            "SELECT id, email, created_at FROM auth.users WHERE id = $1",
            user_id
        )
        
        if not user:
            return None
        
        # Get profile info
        profile = await db.fetch_one(
            "SELECT full_name FROM profiles WHERE user_id = $1",
            user_id
        )
        
        return User(
            id=str(user["id"]),  # Convert UUID to string
            email=user["email"],
            full_name=profile["full_name"] if profile else None,
            created_at=user["created_at"].replace(tzinfo=None)  # Remove timezone info
        )
