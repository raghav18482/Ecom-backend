from typing import List, Optional
from decimal import Decimal
import uuid
from app.core.database import db
from app.models.order import Order, OrderCreate, OrderUpdate, OrderStatusUpdate, OrderItem, OrderItemCreate

class OrderService:
    @staticmethod
    async def create_order(order_data: OrderCreate) -> Order:
        """Create a new order with items"""
        order_id = uuid.uuid4()
        
        # Calculate total amount
        total_amount = sum(item.price * item.quantity for item in order_data.items)
        
        # Create order
        await db.execute(
            """
            INSERT INTO orders (
                id, user_id, total_amount, payment_status, order_status, 
                shipping_address, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
            """,
            order_id,
            order_data.user_id,
            total_amount,
            "pending",
            "processing",
            order_data.shipping_address
        )
        
        # Create order items
        for item in order_data.items:
            item_id = uuid.uuid4()
            await db.execute(
                """
                INSERT INTO order_items (id, order_id, product_id, quantity, price)
                VALUES ($1, $2, $3, $4, $5)
                """,
                item_id,
                order_id,
                item.product_id,
                item.quantity,
                item.price
            )
        
        return await OrderService.get_order_by_id(order_id)
    
    @staticmethod
    async def get_order_by_id(order_id: uuid.UUID) -> Optional[Order]:
        """Get an order by ID with items"""
        order = await db.fetch_one(
            "SELECT * FROM orders WHERE id = $1", order_id
        )
        
        if not order:
            return None
        
        # Get order items
        items = await db.fetch_all(
            "SELECT * FROM order_items WHERE order_id = $1", order_id
        )
        
        order_items = [
            OrderItem(
                id=item["id"],
                order_id=item["order_id"],
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"]
            )
            for item in items
        ]
        
        return Order(
            id=order["id"],
            user_id=order["user_id"],
            total_amount=order["total_amount"],
            payment_status=order["payment_status"],
            order_status=order["order_status"],
            shipping_address=order["shipping_address"],
            created_at=order["created_at"],
            updated_at=order["updated_at"],
            items=order_items
        )
    
    @staticmethod
    async def get_user_orders(user_id: uuid.UUID, limit: int = 20, offset: int = 0) -> List[Order]:
        """Get orders for a specific user"""
        orders = await db.fetch_all(
            """
            SELECT * FROM orders 
            WHERE user_id = $1 
            ORDER BY created_at DESC 
            LIMIT $2 OFFSET $3
            """,
            user_id, limit, offset
        )
        
        result = []
        for order in orders:
            # Get order items
            items = await db.fetch_all(
                "SELECT * FROM order_items WHERE order_id = $1", order["id"]
            )
            
            order_items = [
                OrderItem(
                    id=item["id"],
                    order_id=item["order_id"],
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"]
                )
                for item in items
            ]
            
            result.append(Order(
                id=order["id"],
                user_id=order["user_id"],
                total_amount=order["total_amount"],
                payment_status=order["payment_status"],
                order_status=order["order_status"],
                shipping_address=order["shipping_address"],
                created_at=order["created_at"],
                updated_at=order["updated_at"],
                items=order_items
            ))
        
        return result
    
    @staticmethod
    async def update_order_status(order_id: uuid.UUID, status_update: OrderStatusUpdate) -> Optional[Order]:
        """Update order status"""
        await db.execute(
            """
            UPDATE orders 
            SET order_status = $1, updated_at = NOW()
            WHERE id = $2
            """,
            status_update.order_status,
            order_id
        )
        
        return await OrderService.get_order_by_id(order_id)
    
    @staticmethod
    async def update_order(order_id: uuid.UUID, order_data: OrderUpdate) -> Optional[Order]:
        """Update order details"""
        update_fields = []
        params = []
        param_count = 0
        
        if order_data.payment_status is not None:
            param_count += 1
            update_fields.append(f"payment_status = ${param_count}")
            params.append(order_data.payment_status)
        
        if order_data.order_status is not None:
            param_count += 1
            update_fields.append(f"order_status = ${param_count}")
            params.append(order_data.order_status)
        
        if order_data.shipping_address is not None:
            param_count += 1
            update_fields.append(f"shipping_address = ${param_count}")
            params.append(order_data.shipping_address)
        
        if not update_fields:
            return await OrderService.get_order_by_id(order_id)
        
        param_count += 1
        update_fields.append(f"updated_at = NOW()")
        params.append(order_id)
        
        query = f"""
            UPDATE orders 
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
        """
        
        await db.execute(query, *params)
        
        return await OrderService.get_order_by_id(order_id)
