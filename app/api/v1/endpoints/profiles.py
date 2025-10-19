from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
import uuid
from app.models.profile import Profile, ProfileCreate, ProfileUpdate
from app.services.profile_service import ProfileService
from app.api.dependencies import get_current_user
from app.models.auth import User

router = APIRouter()

@router.get("/{user_id}", response_model=Profile)
async def get_profile(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user)
):
    """Get a user profile by user ID"""
    # Check if user is requesting their own profile
    if user_id != uuid.UUID(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this profile"
        )
    
    profile = await ProfileService.get_profile_by_id(user_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile

@router.put("/{user_id}", response_model=Profile)
async def update_profile(
    user_id: uuid.UUID,
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    # Check if user is updating their own profile
    if user_id != uuid.UUID(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this profile"
        )
    
    try:
        profile = await ProfileService.update_profile(user_id, profile_data)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

@router.post("/", response_model=Profile, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a user profile"""
    # Set user_id from current user
    profile_data.user_id = uuid.UUID(current_user.id)
    
    try:
        profile = await ProfileService.create_profile(profile_data)
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create profile"
        )
