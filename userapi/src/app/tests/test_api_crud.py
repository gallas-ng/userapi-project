import pytest
from httpx import AsyncClient
from app.main import app
from asgi_lifespan import LifespanManager  # NEW

@pytest.mark.asyncio
async def test_crud_flow():
    async with LifespanManager(app):  # triggers startup/shutdown events
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Test creating a user
            response = await ac.post("/users", json={"name": "Bob", "email": "bob@example.com"})
            assert response.status_code == 200
            user = response.json()
            user_id = user["id"]

            # List users
            response = await ac.get("/users")
            assert response.status_code == 200
            users = response.json()
            assert any(u["id"] == user_id for u in users)

            # Get user by ID
            response = await ac.get(f"/users/{user_id}")
            assert response.status_code == 200
            assert response.json()["id"] == user_id

            # Non-existing user
            response = await ac.get("/users/9999")
            assert response.status_code == 404
