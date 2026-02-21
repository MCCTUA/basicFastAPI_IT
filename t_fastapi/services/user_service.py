from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .base_service import BaseService
from src.models.user import Users
from src.schemas.user import UserCreate

class UserService(BaseService[Users]):

    # --- กรณีต้องการเพิ่ม Method พิเศษเฉพาะของ User ---
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> Users:
        # 1. แปลง Pydantic เป็น Dict
        obj_in_data = obj_in.model_dump()
        
        # 2. นำ password มาจัดการ (ในอนาคตต้องใช้ passlib หรือ bcrypt)
        password = obj_in_data.pop("password")
        obj_in_data["hashed_password"] = password + "fake_hash" # จำลองการ hash
        
        # 3. เรียกใช้ create ของแม่ (BaseService)
        # เราต้องสร้างคลาสจำลองหรือส่ง dict เข้าไปแทน obj_in เดิม
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_email(
        self, 
        db: AsyncSession, 
        email: str
        ) -> Optional[Users]:
        """ตัวอย่าง Polymorphism: เพิ่มความสามารถที่แม่ไม่มี เช่น ค้นหาด้วย email"""
        result = await db.execute(
            select(
                self.model
                ).filter(
                    self.model.email == email
                    )
                )
        return result.scalars().first()

# สร้าง Instance เพื่อนำไปเรียกใช้ใน Router
user_service = UserService(Users)