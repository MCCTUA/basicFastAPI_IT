from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from src.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,
    pool_size=10,        # จำนวนการเชื่อมต่อสูงสุดที่เปิดค้างไว้
    max_overflow=20      # จำนวนที่ขยายได้ชั่วคราวเมื่อ pool เต็ม
    )

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session