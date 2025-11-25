from .db import db

async def create_user(name: str, email: str):
    row = await db.fetchrow(
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email;",
        name, email
    )
    return dict(row)

async def get_user(user_id: int):
    row = await db.fetchrow(
        "SELECT id, name, email FROM users WHERE id=$1;",
        user_id
    )
    return dict(row) if row else None

async def list_users():
    rows = await db.fetch(
        "SELECT id, name, email FROM users ORDER BY id ASC;"
    )
    return [dict(r) for r in rows]
