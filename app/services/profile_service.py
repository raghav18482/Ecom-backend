from typing import Optional
import uuid
from app.core.database import db
from app.models.profile import Profile, ProfileCreate, ProfileUpdate

class ProfileService:
    @staticmethod
    async def create_profile(profile_data: ProfileCreate) -> Profile:
        """Create a new profile"""
        await db.execute(
            """
            INSERT INTO profiles (id, user_id, full_name, phone, address, created_at)
            VALUES ($1, $2, $3, $4, $5, NOW())
            """,
            profile_data.user_id,
            profile_data.user_id,
            profile_data.full_name,
            profile_data.phone,
            profile_data.address
        )
        
        return await ProfileService.get_profile_by_id(profile_data.user_id)
    
    @staticmethod
    async def get_profile_by_id(user_id: uuid.UUID) -> Optional[Profile]:
        """Get a profile by user ID"""
        profile = await db.fetch_one(
            "SELECT * FROM profiles WHERE user_id = $1", user_id
        )
        
        if not profile:
            return None
        
        return Profile(
            id=profile["id"],
            user_id=profile["user_id"],
            full_name=profile["full_name"],
            phone=profile["phone"],
            address=profile["address"],
            created_at=profile["created_at"]
        )
    
    @staticmethod
    async def update_profile(user_id: uuid.UUID, profile_data: ProfileUpdate) -> Optional[Profile]:
        """Update a profile"""
        update_fields = []
        params = []
        param_count = 0
        
        if profile_data.full_name is not None:
            param_count += 1
            update_fields.append(f"full_name = ${param_count}")
            params.append(profile_data.full_name)
        
        if profile_data.phone is not None:
            param_count += 1
            update_fields.append(f"phone = ${param_count}")
            params.append(profile_data.phone)
        
        if profile_data.address is not None:
            param_count += 1
            update_fields.append(f"address = ${param_count}")
            params.append(profile_data.address)
        
        if not update_fields:
            return await ProfileService.get_profile_by_id(user_id)
        
        params.append(user_id)
        
        query = f"""
            UPDATE profiles 
            SET {', '.join(update_fields)}
            WHERE user_id = ${param_count + 1}
        """
        
        await db.execute(query, *params)
        
        return await ProfileService.get_profile_by_id(user_id)
