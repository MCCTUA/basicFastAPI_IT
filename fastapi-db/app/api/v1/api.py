from fastapi import APIRouter
from app.api.v1.endpoints import users, items

# สร้าง API Router หลัก
api_router = APIRouter()

# รวม Route ของ Users
api_router.include_router(users.router, prefix="/users", tags=["users"])

# รวม Route ของ Items
api_router.include_router(items.router, prefix="/items", tags=["items"])
