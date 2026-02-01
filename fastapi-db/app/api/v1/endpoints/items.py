from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas import item as item_schema
from app.services import item_service

# สร้าง Router สำหรับ Item Endpoints
router = APIRouter()


# Endpoint ดึงรายชื่อไอเท็มทั้งหมด
@router.get("/", response_model=List[item_schema.Item])
async def read_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(deps.get_db)
):
    # เพิ่ม await
    items = await item_service.get_items(db, skip=skip, limit=limit)
    return items


# Endpoint สร้างไอเท็มใหม่สำหรับผู้ใช้
@router.post("/{user_id}/items/", response_model=item_schema.Item)
async def create_item_for_user(
    user_id: int, item: item_schema.ItemCreate, db: AsyncSession = Depends(deps.get_db)
):
    # เพิ่ม await
    return await item_service.create_user_item(db=db, item=item, user_id=user_id)
