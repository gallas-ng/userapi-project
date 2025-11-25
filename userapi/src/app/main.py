from fastapi import FastAPI

app = FastAPI(title="UserAPI")

@app.get("/health")
async def health():
    return {"status": "ok"}