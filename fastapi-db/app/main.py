from fastapi import FastAPI

# นำเข้า BaseModel จาก Pydantic เพื่อใช้ในการสร้างโมเดลข้อมูล
from pydantic import BaseModel

# นำเข้า get_scalar_api_reference จาก scalar_fastapi  ช่วยในการสร้างเอกสาร API
from scalar_fastapi import get_scalar_api_reference

# Create an instance of the FastAPI application
app = FastAPI()


# สร้างเส้นทาง (route) สำหรับ root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI with uv!"}


# สร้างเส้นทางสำหรับดึงเอกสาร API reference (scalar API reference)
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        # title="My FastAPI Scalar API Reference",
        title=app.title,
    )
