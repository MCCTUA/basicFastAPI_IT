from fastapi import APIRouter, Depends
from app.api import deps
from app.api.v1.endpoints import users, items, auth

# สร้าง API Router หลัก
api_router = APIRouter()

# รวม Route ของ Auth
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# รวม Route ของ Users (Protected)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(deps.get_current_active_user)],
)

# รวม Route ของ Items (Protected)
api_router.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(deps.get_current_active_user)],
)
