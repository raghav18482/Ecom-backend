from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import uuid

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    images: List[str] = Field(default_factory=list)
    color: Optional[str] = None
    size: List[str] = Field(default_factory=list)
    material: Optional[str] = None
    fit_type: Optional[str] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[Decimal] = Field(None, ge=0, le=5)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    images: Optional[List[str]] = None
    color: Optional[str] = None
    size: Optional[List[str]] = None
    material: Optional[str] = None
    fit_type: Optional[str] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[Decimal] = Field(None, ge=0, le=5)

class Product(ProductBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductFilter(BaseModel):
    category: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    gender: Optional[str] = None
    fit_type: Optional[str] = None
    min_rating: Optional[Decimal] = None
    search: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
