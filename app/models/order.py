from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import uuid
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"

class OrderStatus(str, Enum):
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItemBase(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: uuid.UUID
    order_id: uuid.UUID

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: uuid.UUID
    total_amount: Decimal = Field(..., gt=0)
    payment_status: PaymentStatus = PaymentStatus.PENDING
    order_status: OrderStatus = OrderStatus.PROCESSING
    shipping_address: str = Field(..., min_length=1)

class OrderCreate(BaseModel):
    user_id: uuid.UUID
    items: List[OrderItemCreate] = Field(..., min_items=1)
    shipping_address: str = Field(..., min_length=1)

class OrderUpdate(BaseModel):
    payment_status: Optional[PaymentStatus] = None
    order_status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = Field(None, min_length=1)

class Order(OrderBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    items: List[OrderItem] = []

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    order_status: OrderStatus
