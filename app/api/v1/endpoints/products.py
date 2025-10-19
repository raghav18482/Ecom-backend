from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from decimal import Decimal
import uuid
from app.models.product import Product, ProductCreate, ProductUpdate, ProductFilter
from app.services.product_service import ProductService
from app.api.dependencies import get_current_user, get_current_user_optional
from app.models.auth import User

router = APIRouter()

@router.get("/", response_model=List[Product])
async def get_products(
    category: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    min_price: Optional[Decimal] = Query(None),
    max_price: Optional[Decimal] = Query(None),
    gender: Optional[str] = Query(None),
    fit_type: Optional[str] = Query(None),
    min_rating: Optional[Decimal] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all products with optional filters"""
    filters = ProductFilter(
        category=category,
        color=color,
        size=size,
        min_price=min_price,
        max_price=max_price,
        gender=gender,
        fit_type=fit_type,
        min_rating=min_rating,
        search=search,
        limit=limit,
        offset=offset
    )
    
    try:
        products = await ProductService.get_products(filters)
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch products"
        )

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: uuid.UUID):
    """Get a specific product by ID"""
    product = await ProductService.get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new product (admin only)"""
    # In a real app, you'd check if user is admin
    # For now, we'll allow any authenticated user to create products
    try:
        product = await ProductService.create_product(product_data)
        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: uuid.UUID,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a product (admin only)"""
    # In a real app, you'd check if user is admin
    try:
        product = await ProductService.update_product(product_id, product_data)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product"
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: uuid.UUID,
    current_user: User = Depends(get_current_user)
):
    """Delete a product (admin only)"""
    # In a real app, you'd check if user is admin
    try:
        success = await ProductService.delete_product(product_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product"
        )
