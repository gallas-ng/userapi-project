import pytest
from httpx import AsyncClient
from app.main import app
import asyncio

@pytest.mark.asyncio
async def test_crud_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 1️⃣ Test creating a user
        response = await ac.post("/users", json={"name": "Bob", "email": "bob@example.com"})
        assert response.status_code == 200
        user = response.json()
        assert user["name"] == "Bob"
        assert user["email"] == "bob@example.com"
        user_id = user["id"]

        # 2️⃣ Test listing users
        response = await ac.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert any(u["id"] == user_id for u in users)

        # 3️⃣ Test getting user by ID
        response = await ac.get(f"/users/{user_id}")
        assert response.status_code == 200
        user_by_id = response.json()
        assert user_by_id["id"] == user_id

        # 4️⃣ Test getting non-existing user
        response = await ac.get("/users/9999")
        assert response.status_code == 404
