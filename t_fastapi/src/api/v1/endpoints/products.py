from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from services import product_service

router = APIRouter()

@router.get("/")
async def get_products(db: AsyncSession = Depends(get_db)):
    return await product_service.get_multi(db)