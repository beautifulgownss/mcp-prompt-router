from fastapi import FastAPI
from app.routers.route import router as route_router

app = FastAPI(title="MCP Prompt Router", version="0.1.0")
app.include_router(route_router)

@app.get("/health")
def health():
    return {"ok": True}