from fastapi import FastAPI
from src.api.v1.api import api_router

app = FastAPI(title="Gismo ERP API")

# ลงทะเบียน Router ทั้งหมดภายใต้ prefix /api/v1
app.include_router(api_router, prefix="/api/v1")