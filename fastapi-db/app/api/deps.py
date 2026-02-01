"""
หน้าที่ของไฟล์นี้คือการจัดการ Dependency Injection สำหรับการเชื่อมต่อฐานข้อมูล
ในกรณีนี้ เราจะเปลี่ยนจากการใช้ Session ปกติเป็น AsyncSession
เพื่อให้สามารถทำงานแบบ Asynchronous ได้เต็มที่ กับ FastAPI และ SQLAlchemy
"""

from typing import AsyncGenerator
from app.db.session import SessionLocal


# เปลี่ยนจาก Generator ธรรมดา เป็น AsyncGenerator
async def get_db() -> AsyncGenerator:
    # SessionLocal() เป็น AsyncSession ที่เราสร้างไว้ เป็นการดึง session ที่เชื่อมต่อกับ DB มาใช้
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            # SessionLocal จะปิดตัวเองอัตโนมัติเมื่อจบ async with
            # หรือถ้าไม่ได้ใช้ context manager ต้อง await db.close() เอง
            # จะได้คืน ทรัพยากรกลับไปยัง connection pool ไม่เปลื้อง memory
            pass
