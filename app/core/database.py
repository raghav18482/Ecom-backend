import asyncpg
import logging
import os
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

# Detect serverless runtime (Vercel)
IS_SERVERLESS = os.getenv("VERCEL", "false").lower() == "true"

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Create a pool only for local/dev environments."""
        if self.pool or IS_SERVERLESS:
            return

        try:
            logger.info(f"Connecting to database URL: {settings.DATABASE_URL}")
            self.pool = await asyncpg.create_pool(
                dsn=settings.DATABASE_URL,
                min_size=1,
                max_size=2,
                command_timeout=60,
                statement_cache_size=0
            )
            logger.info("✅ Database pool created successfully (local)")
        except Exception as e:
            logger.exception(f"❌ Failed to connect to database: {e}")
            self.pool = None
            raise

    async def _get_connection(self):
        """Get a connection based on environment."""
        if IS_SERVERLESS:
            return await asyncpg.connect(settings.DATABASE_URL)
        else:
            await self.connect()
            return await self.pool.acquire()

    async def _release_connection(self, conn):
        """Release or close the connection."""
        if IS_SERVERLESS:
            await conn.close()
        else:
            await self.pool.release(conn)

    async def fetch_all(self, query: str, *args):
        conn = await self._get_connection()
        try:
            return await conn.fetch(query, *args)
        finally:
            await self._release_connection(conn)

    async def fetch_one(self, query: str, *args):
        conn = await self._get_connection()
        try:
            return await conn.fetchrow(query, *args)
        finally:
            await self._release_connection(conn)

    async def execute(self, query: str, *args):
        conn = await self._get_connection()
        try:
            return await conn.execute(query, *args)
        finally:
            await self._release_connection(conn)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
            logger.info("🛑 Database pool closed")

# global instance
db = Database()

async def init_db():
    await db.connect()

async def close_db():
    await db.disconnect()