from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# app/core/config.py import settings
from app.core.config import settings

# 1. สร้าง Async Engine (settings.DATABASE_URL มาจากไฟล์ config.py, echo=True เพื่อแสดง SQL log)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 2. สร้าง Session Factory
# autocommit=False: ต้องเรียก commit() เอง : commit คือ การบันทึกการเปลี่ยนแปลงลงฐานข้อมูล
# autoflush=False: ต้องเรียก flush() เอง : flush คือ การซิงค์ข้อมูลกับฐานข้อมูลก่อน commit
# bind=engine: ผูกกับ engine ที่สร้างขึ้น : engine คือ ตัวเชื่อมต่อกับฐานข้อมูล
# class_=AsyncSession: ใช้ AsyncSession สำหรับ session แบบอะซิงโครนัส
SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# 3. Dependency สำหรับใช้ใน API Endpoint (Dependency Injection)
# ใช้ yield เพื่อสร้าง session และปิด session อัตโนมัติเมื่อเสร็จงาน ทำให้ไม่ต้องปิด session เอง และช่วยจัดการ connection pool ได้ดีขึ้น
# get_db จะถูกใช้ใน endpoint เพื่อรับ session
async def get_db():
    async with SessionLocal() as session:
        yield session
