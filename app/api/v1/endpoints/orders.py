from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
import uuid
from app.models.order import Order, OrderCreate, OrderUpdate, OrderStatusUpdate
from app.services.order_service import OrderService
from app.api.dependencies import get_current_user
from app.models.auth import User

router = APIRouter()

@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new order"""
    try:
        # Set user_id from current user
        order_data.user_id = uuid.UUID(current_user.id)
        order = await OrderService.create_order(order_data)
        return order
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: uuid.UUID,
    current_user: User = Depends(get_current_user)
):
    """Get a specific order by ID"""
    order = await OrderService.get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns this order
    if order.user_id != uuid.UUID(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    return order

@router.get("/user/{user_id}", response_model=List[Order])
async def get_user_orders(
    user_id: uuid.UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user)
):
    """Get orders for a specific user"""
    # Check if user is requesting their own orders
    if user_id != uuid.UUID(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these orders"
        )
    
    try:
        orders = await OrderService.get_user_orders(user_id, limit, offset)
        return orders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch orders"
        )

@router.put("/{order_id}/status", response_model=Order)
async def update_order_status(
    order_id: uuid.UUID,
    status_update: OrderStatusUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update order status (admin only)"""
    # In a real app, you'd check if user is admin
    try:
        order = await OrderService.update_order_status(order_id, status_update)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update order status"
        )

@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: uuid.UUID,
    order_data: OrderUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update order details (admin only)"""
    # In a real app, you'd check if user is admin
    try:
        order = await OrderService.update_order(order_id, order_data)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update order"
        )
