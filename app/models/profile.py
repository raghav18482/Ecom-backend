from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class ProfileBase(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None

class ProfileCreate(ProfileBase):
    user_id: uuid.UUID

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
