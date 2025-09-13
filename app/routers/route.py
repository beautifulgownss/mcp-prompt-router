from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, Optional
from app.services.router import route_task

router = APIRouter(prefix="/v1", tags=["router"])

class RouteRequest(BaseModel):
    task: str
    inputs: Optional[Dict[str, Any]] = None
    constraints: Optional[Dict[str, Any]] = None
    profile: Optional[str] = "fast-cheap-safe"
    metadata: Optional[Dict[str, Any]] = None

@router.post("/route")
def route(req: RouteRequest):
    return route_task(req.task, req.inputs, req.constraints, req.profile)