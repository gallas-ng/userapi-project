import asyncpg
import os


DB_USER = os.getenv("DATABASE_USER", "vagrant")
DB_PASS = os.getenv("DATABASE_PASSWORD", "password")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_NAME = os.getenv("DATABASE_NAME", "userdb")
DATABASE_URL = os.getenv("DATABASE_URL") or (
    f"postgresql://{DB_USER}:{DB_PASS}"
    f"@{DB_HOST}:5432/{DB_NAME}"
)

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(DATABASE_URL)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

db = Database()

async def init_db():
    # Ensure connection
    await db.connect()

    # Create table if not exists
    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
    """)
