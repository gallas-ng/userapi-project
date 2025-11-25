from fastapi import FastAPI, HTTPException
from .db import init_db, db
from .schemas import UserCreate, UserOut
from .crud import create_user, get_user, list_users

app = FastAPI(title="UserAPI")

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/users", response_model=UserOut)
async def api_create_user(payload: UserCreate):
    user = await create_user(payload.name, payload.email)
    return user

@app.get("/users/{user_id}", response_model=UserOut)
async def api_get_user(user_id: int):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=list[UserOut])
async def api_list_users():
    return await list_users()
