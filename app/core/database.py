import asyncpg
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if self.pool:
            return
        try:
            logger.info(f"Connecting to database URL: {settings.DATABASE_URL}")
            self.pool = await asyncpg.create_pool(
                settings.DATABASE_URL,
                min_size=1,
                max_size=2,  # reduced for serverless
                command_timeout=60,
                statement_cache_size=0
            )
            logger.info("✅ Database pool created")
        except Exception as e:
            logger.exception(f"❌ Failed to connect to database: {e}")
            self.pool = None
            # Optionally: retry with delay (not just raise)
            raise


    async def _ensure_connected(self):
        """Ensure pool is ready before any query"""
        if not self.pool:
            await self.connect()

    async def fetch_all(self, query: str, *args):
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetch_one(self, query: str, *args):
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def execute(self, query: str, *args):
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
            logger.info("Database connection pool closed")

# global instance
db = Database()

async def init_db():
    await db.connect()

async def close_db():
    await db.disconnect()