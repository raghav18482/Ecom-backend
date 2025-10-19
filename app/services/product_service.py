from typing import List, Optional
from decimal import Decimal
import uuid
from app.core.database import db
from app.models.product import Product, ProductCreate, ProductUpdate, ProductFilter

class ProductService:
    @staticmethod
    async def create_product(product_data: ProductCreate) -> Product:
        """Create a new product"""
        product_id = uuid.uuid4()
        
        await db.execute(
            """
            INSERT INTO products (
                id, name, description, price, stock, images, color, size, 
                material, fit_type, gender, category, rating, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, NOW(), NOW())
            """,
            product_id,
            product_data.name,
            product_data.description,
            product_data.price,
            product_data.stock,
            product_data.images,
            product_data.color,
            product_data.size,
            product_data.material,
            product_data.fit_type,
            product_data.gender,
            product_data.category,
            product_data.rating
        )
        
        return await ProductService.get_product_by_id(product_id)
    
    @staticmethod
    async def get_product_by_id(product_id: uuid.UUID) -> Optional[Product]:
        """Get a product by ID"""
        product = await db.fetch_one(
            "SELECT * FROM products WHERE id = $1", product_id
        )
        
        if not product:
            return None
        
        return Product(
            id=product["id"],
            name=product["name"],
            description=product["description"],
            price=product["price"],
            stock=product["stock"],
            images=product["images"] or [],
            color=product["color"],
            size=product["size"] or [],
            material=product["material"],
            fit_type=product["fit_type"],
            gender=product["gender"],
            category=product["category"],
            rating=product["rating"],
            created_at=product["created_at"],
            updated_at=product["updated_at"]
        )
    
    @staticmethod
    async def get_products(filters: ProductFilter) -> List[Product]:
        """Get products with filters"""
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        param_count = 0
        
        if filters.category:
            param_count += 1
            query += f" AND category = ${param_count}"
            params.append(filters.category)
        
        if filters.color:
            param_count += 1
            query += f" AND color = ${param_count}"
            params.append(filters.color)
        
        if filters.size:
            param_count += 1
            query += f" AND ${param_count} = ANY(size)"
            params.append(filters.size)
        
        if filters.min_price:
            param_count += 1
            query += f" AND price >= ${param_count}"
            params.append(filters.min_price)
        
        if filters.max_price:
            param_count += 1
            query += f" AND price <= ${param_count}"
            params.append(filters.max_price)
        
        if filters.gender:
            param_count += 1
            query += f" AND gender = ${param_count}"
            params.append(filters.gender)
        
        if filters.fit_type:
            param_count += 1
            query += f" AND fit_type = ${param_count}"
            params.append(filters.fit_type)
        
        if filters.min_rating:
            param_count += 1
            query += f" AND rating >= ${param_count}"
            params.append(filters.min_rating)
        
        if filters.search:
            param_count += 1
            query += f" AND (name ILIKE ${param_count} OR description ILIKE ${param_count})"
            search_term = f"%{filters.search}%"
            params.extend([search_term, search_term])
        
        query += f" ORDER BY created_at DESC LIMIT {filters.limit} OFFSET {filters.offset}"
        
        products = await db.fetch_all(query, *params)
        
        return [
            Product(
                id=product["id"],
                name=product["name"],
                description=product["description"],
                price=product["price"],
                stock=product["stock"],
                images=product["images"] or [],
                color=product["color"],
                size=product["size"] or [],
                material=product["material"],
                fit_type=product["fit_type"],
                gender=product["gender"],
                category=product["category"],
                rating=product["rating"],
                created_at=product["created_at"],
                updated_at=product["updated_at"]
            )
            for product in products
        ]
    
    @staticmethod
    async def update_product(product_id: uuid.UUID, product_data: ProductUpdate) -> Optional[Product]:
        """Update a product"""
        # Build dynamic update query
        update_fields = []
        params = []
        param_count = 0
        
        if product_data.name is not None:
            param_count += 1
            update_fields.append(f"name = ${param_count}")
            params.append(product_data.name)
        
        if product_data.description is not None:
            param_count += 1
            update_fields.append(f"description = ${param_count}")
            params.append(product_data.description)
        
        if product_data.price is not None:
            param_count += 1
            update_fields.append(f"price = ${param_count}")
            params.append(product_data.price)
        
        if product_data.stock is not None:
            param_count += 1
            update_fields.append(f"stock = ${param_count}")
            params.append(product_data.stock)
        
        if product_data.images is not None:
            param_count += 1
            update_fields.append(f"images = ${param_count}")
            params.append(product_data.images)
        
        if product_data.color is not None:
            param_count += 1
            update_fields.append(f"color = ${param_count}")
            params.append(product_data.color)
        
        if product_data.size is not None:
            param_count += 1
            update_fields.append(f"size = ${param_count}")
            params.append(product_data.size)
        
        if product_data.material is not None:
            param_count += 1
            update_fields.append(f"material = ${param_count}")
            params.append(product_data.material)
        
        if product_data.fit_type is not None:
            param_count += 1
            update_fields.append(f"fit_type = ${param_count}")
            params.append(product_data.fit_type)
        
        if product_data.gender is not None:
            param_count += 1
            update_fields.append(f"gender = ${param_count}")
            params.append(product_data.gender)
        
        if product_data.category is not None:
            param_count += 1
            update_fields.append(f"category = ${param_count}")
            params.append(product_data.category)
        
        if product_data.rating is not None:
            param_count += 1
            update_fields.append(f"rating = ${param_count}")
            params.append(product_data.rating)
        
        if not update_fields:
            return await ProductService.get_product_by_id(product_id)
        
        param_count += 1
        update_fields.append(f"updated_at = NOW()")
        params.append(product_id)
        
        query = f"""
            UPDATE products 
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING *
        """
        
        result = await db.fetch_one(query, *params)
        
        if not result:
            return None
        
        return Product(
            id=result["id"],
            name=result["name"],
            description=result["description"],
            price=result["price"],
            stock=result["stock"],
            images=result["images"] or [],
            color=result["color"],
            size=result["size"] or [],
            material=result["material"],
            fit_type=result["fit_type"],
            gender=result["gender"],
            category=result["category"],
            rating=result["rating"],
            created_at=result["created_at"],
            updated_at=result["updated_at"]
        )
    
    @staticmethod
    async def delete_product(product_id: uuid.UUID) -> bool:
        """Delete a product"""
        result = await db.execute(
            "DELETE FROM products WHERE id = $1", product_id
        )
        return "DELETE 1" in result
