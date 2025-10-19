import asyncpg
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Create database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                settings.DATABASE_URL,
                min_size=1,
                max_size=10,
                command_timeout=60,
                statement_cache_size=0  # Disable prepared statements for pgbouncer compatibility
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create database connection pool: {e}")
            raise

    async def disconnect(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    async def fetch_one(self, query: str, *args):
        """Fetch a single row"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetch_all(self, query: str, *args):
        """Fetch all rows"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query: str, *args):
        """Execute a query"""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetchval(self, query: str, *args):
        """Fetch a single value"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

# Global database instance
db = Database()

async def init_db():
    """Initialize database connection"""
    await db.connect()

async def close_db():
    """Close database connection"""
    await db.disconnect()
