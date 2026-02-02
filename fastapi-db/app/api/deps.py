"""
หน้าที่ของไฟล์นี้คือการจัดการ Dependency Injection สำหรับการเชื่อมต่อฐานข้อมูล
ในกรณีนี้ เราจะเปลี่ยนจากการใช้ Session ปกติเป็น AsyncSession
เพื่อให้สามารถทำงานแบบ Asynchronous ได้เต็มที่ กับ FastAPI และ SQLAlchemy
"""

from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import config
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload
from app.services import user_service

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")


# เปลี่ยนจาก Generator ธรรมดา เป็น AsyncGenerator
async def get_db() -> AsyncGenerator:
    # SessionLocal() เป็น AsyncSession ที่เราสร้างไว้ เป็นการดึง session ที่เชื่อมต่อกับ DB มาใช้
    # async with จะช่วยจัดการการเปิด-ปิด session อัตโนมัติ
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            # SessionLocal จะปิดตัวเองอัตโนมัติเมื่อจบ async with
            # หรือถ้าไม่ได้ใช้ context manager ต้อง await db.close() เอง
            # จะได้คืน ทรัพยากรกลับไปยัง connection pool ไม่เปลื้อง memory
            pass


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await user_service.get_user(db, user_id=int(token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
