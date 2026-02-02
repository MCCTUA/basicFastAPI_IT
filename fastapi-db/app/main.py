from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# นำเข้า BaseModel จาก Pydantic เพื่อใช้ในการสร้างโมเดลข้อมูล
from pydantic import BaseModel

# นำเข้า api_router ที่เราสร้างไว้ใน api/v1/api.py
from app.api.v1.api import api_router
from app.core.limiter import limiter

# นำเข้า get_scalar_api_reference จาก scalar_fastapi  ช่วยในการสร้างเอกสาร API
from scalar_fastapi import get_scalar_api_reference

# Create an instance of the FastAPI application
app = FastAPI(title="My FastAPI App")

# ตั้งค่า Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# นำ Router ทั้งหมดมาแปะที่ /api/v1
app.include_router(api_router, prefix="/api/v1")


# สร้างเส้นทางสำหรับดึงเอกสาร API reference (scalar API reference)
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,  # [cite: 119]
        title=app.title,  # [cite: 121]
        # เพิ่มเติม: มั่นใจว่าไม่ได้มีการ override security
        # หรือลองใช้เทคนิคการจำ Token ผ่าน Browser Session
    )
