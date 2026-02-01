from typing import Optional
from pydantic import BaseModel, EmailStr


# Shared properties เอาไปใช้ ที่อื่นได้
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive via API on creation
# บังคับให้มี email กับ password เวลาสร้าง user ใหม่
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
# อนุญาตให้แก้ไขได้ โดยกำหนให้ password เป็น optional
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties to return via API
class User(UserBase):
    # เวลา return จะ return id ออกไปใช้งาน
    id: int

    class Config:
        from_attributes = True  # รองรับ ORM mode (v2 ใช้ config นี้)
