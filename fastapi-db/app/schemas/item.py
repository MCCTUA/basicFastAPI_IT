from typing import Optional
from pydantic import BaseModel


# class นี้มีหน้าที่ เก็บ schema ของ Item เพื่อ shared properties ไปใช้ที่อื่น
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# กำหนดให้ตอนสร้งา item ใหม่ ต้องมี title
class ItemCreate(ItemBase):
    title: str


# เราใส่ pass เพราะเราไม่ต้องการบังคับฟิลด์ใดๆ ในการอัพเดต
class ItemUpdate(ItemBase):
    pass


# เรา return id กับ owner_id ออกไปใช้งานด้วย
class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # รองรับ ORM mode (v2 ใช้ config นี้)
