#!/usr/bin/env python3
"""
Seed script to populate the database with sample hoodie products
Run this script to add sample data to your Supabase database
"""

import asyncio
import asyncpg
from decimal import Decimal
from app.core.config import settings

# Sample hoodie products data
SAMPLE_PRODUCTS = [
    {
        "name": "Classic Black Hoodie",
        "description": "A timeless black hoodie made from premium cotton blend. Perfect for everyday wear with a comfortable fit and durable construction.",
        "price": Decimal("49.99"),
        "stock": 50,
        "images": ["https://example.com/black-hoodie-1.jpg", "https://example.com/black-hoodie-2.jpg"],
        "color": "Black",
        "size": ["S", "M", "L", "XL", "XXL"],
        "material": "80% Cotton, 20% Polyester",
        "fit_type": "Regular",
        "gender": "Unisex",
        "category": "Classic",
        "rating": Decimal("4.5")
    },
    {
        "name": "Vintage White Hoodie",
        "description": "A vintage-inspired white hoodie with a relaxed fit. Features a soft fleece lining and ribbed cuffs for ultimate comfort.",
        "price": Decimal("54.99"),
        "stock": 35,
        "images": ["https://example.com/white-hoodie-1.jpg", "https://example.com/white-hoodie-2.jpg"],
        "color": "White",
        "size": ["S", "M", "L", "XL"],
        "material": "100% Cotton",
        "fit_type": "Oversized",
        "gender": "Unisex",
        "category": "Vintage",
        "rating": Decimal("4.3")
    },
    {
        "name": "Navy Blue Athletic Hoodie",
        "description": "Designed for active lifestyles, this navy blue hoodie features moisture-wicking fabric and a modern athletic cut.",
        "price": Decimal("69.99"),
        "stock": 40,
        "images": ["https://example.com/navy-hoodie-1.jpg", "https://example.com/navy-hoodie-2.jpg"],
        "color": "Navy Blue",
        "size": ["S", "M", "L", "XL", "XXL"],
        "material": "Polyester Blend",
        "fit_type": "Athletic",
        "gender": "Unisex",
        "category": "Athletic",
        "rating": Decimal("4.7")
    },
    {
        "name": "Forest Green Eco Hoodie",
        "description": "Made from sustainable materials, this forest green hoodie is perfect for environmentally conscious consumers.",
        "price": Decimal("79.99"),
        "stock": 25,
        "images": ["https://example.com/green-hoodie-1.jpg", "https://example.com/green-hoodie-2.jpg"],
        "color": "Forest Green",
        "size": ["S", "M", "L", "XL"],
        "material": "Organic Cotton",
        "fit_type": "Regular",
        "gender": "Unisex",
        "category": "Eco-Friendly",
        "rating": Decimal("4.6")
    },
    {
        "name": "Charcoal Grey Premium Hoodie",
        "description": "Our premium charcoal grey hoodie features a luxurious feel with reinforced seams and a modern minimalist design.",
        "price": Decimal("89.99"),
        "stock": 30,
        "images": ["https://example.com/charcoal-hoodie-1.jpg", "https://example.com/charcoal-hoodie-2.jpg"],
        "color": "Charcoal Grey",
        "size": ["S", "M", "L", "XL", "XXL"],
        "material": "Premium Cotton Blend",
        "fit_type": "Slim Fit",
        "gender": "Unisex",
        "category": "Premium",
        "rating": Decimal("4.8")
    }
]

async def create_tables():
    """Create necessary tables if they don't exist"""
    conn = await asyncpg.connect(settings.DATABASE_URL)
    
    try:
        # Create products table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name TEXT NOT NULL,
                description TEXT,
                price NUMERIC(10,2) NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                images TEXT[] DEFAULT '{}',
                color TEXT,
                size TEXT[] DEFAULT '{}',
                material TEXT,
                fit_type TEXT,
                gender TEXT,
                category TEXT,
                rating NUMERIC(3,2),
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        
        # Create profiles table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL,
                full_name TEXT,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Create orders table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL,
                total_amount NUMERIC(10,2) NOT NULL,
                payment_status TEXT DEFAULT 'pending',
                order_status TEXT DEFAULT 'processing',
                shipping_address TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Create order_items table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                quantity INTEGER NOT NULL,
                price NUMERIC(10,2) NOT NULL
            );
        """)
        
        # Skip auth.users table creation as it's managed by Supabase
        # The auth.users table is already created by Supabase
        
        print("✅ Tables created successfully")
        
    finally:
        await conn.close()

async def seed_products():
    """Seed the database with sample products"""
    conn = await asyncpg.connect(settings.DATABASE_URL)
    
    try:
        # Clear existing products
        await conn.execute("DELETE FROM products")
        print("🗑️  Cleared existing products")
        
        # Insert sample products
        for product in SAMPLE_PRODUCTS:
            await conn.execute("""
                INSERT INTO products (
                    name, description, price, stock, images, color, size,
                    material, fit_type, gender, category, rating
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            """, 
                product["name"],
                product["description"],
                product["price"],
                product["stock"],
                product["images"],
                product["color"],
                product["size"],
                product["material"],
                product["fit_type"],
                product["gender"],
                product["category"],
                product["rating"]
            )
        
        print(f"✅ Seeded {len(SAMPLE_PRODUCTS)} products successfully")
        
    finally:
        await conn.close()

async def main():
    """Main function to run the seed script"""
    print("🌱 Starting database seeding...")
    
    try:
        # Create tables
        await create_tables()
        
        # Seed products
        await seed_products()
        
        print("🎉 Database seeding completed successfully!")
        print("\n📊 Sample products added:")
        for i, product in enumerate(SAMPLE_PRODUCTS, 1):
            print(f"  {i}. {product['name']} - ${product['price']}")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
