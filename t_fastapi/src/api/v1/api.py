from fastapi import APIRouter
from src.api.v1.endpoints import users, products

api_router = APIRouter()

# รวม Router และกำหนด Path ให้ชัดเจน
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])