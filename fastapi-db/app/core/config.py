from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # กำหนด Default ได้เฉพาะค่าที่ไม่ใช่ความลับ
    PROJECT_NAME: str = "My FastAPI Project"

    DATABASE_URL: str

    class Config:
        env_file = ".env"
        # env_file_encoding = "utf-8"  # กำหนด encoding ของไฟล์ .env


settings = Settings()
