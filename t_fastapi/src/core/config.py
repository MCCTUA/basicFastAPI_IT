from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. กำหนดชื่อตัวแปรและชนิดข้อมูล (ต้องตรงกับใน .env)
    DATABASE_URL: str
    SECRET_KEY: str
    PROJECT_NAME: str = "T_FastAPI"

    POSTGRES_PASSWORD: str 
    POSTGRES_DB: str

    # 2. ตั้งค่าให้ไปอ่านไฟล์ .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # สั่งให้ Pydantic มองข้ามตัวแปรที่ไม่ได้นิยามไว้
    )

# 3. สร้าง Instance เพื่อเรียกไปใช้งาน
settings = Settings()