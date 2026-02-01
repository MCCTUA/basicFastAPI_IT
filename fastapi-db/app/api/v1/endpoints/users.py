from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  # เปลี่ยน import เป็น AsyncSession

from app.api import deps  # หรือตำแหน่งที่คุณเก็บ get_db
from app.schemas import user as user_schema
from app.services import user_service

# สร้าง Router สำหรับ User Endpoints
router = APIRouter()


# Endpoint ดึงรายชื่อผู้ใช้ทั้งหมด
@router.get("/", response_model=List[user_schema.User])
async def read_users(  # เพิ่ม async
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db),  # เปลี่ยน Type hint
):
    # เพิ่ม await
    users = await user_service.get_users(db, skip=skip, limit=limit)
    return users


# Endpoint สร้างผู้ใช้ใหม่
@router.post("/", response_model=user_schema.User)
async def create_user(  # เพิ่ม async
    user: user_schema.UserCreate, db: AsyncSession = Depends(deps.get_db)
):
    # เพิ่ม await
    db_user = await user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_service.create_user(db=db, user=user)


# Endpoint ดึงข้อมูลผู้ใช้ตาม ID
@router.get("/{user_id}", response_model=user_schema.User)
async def read_user(user_id: int, db: AsyncSession = Depends(deps.get_db)):  # เพิ่ม async
    # เพิ่ม await
    db_user = await user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
