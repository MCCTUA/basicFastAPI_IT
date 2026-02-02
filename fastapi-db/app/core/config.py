from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # กำหนด Default ได้เฉพาะค่าที่ไม่ใช่ความลับ
    PROJECT_NAME: str = "My FastAPI Project"

    # Pydantic จะบังคับให้ไปหาค่านี้จากไฟล์ .env เท่านั้น ถ้าหาไม่เจอโปรแกรมจะ Error
    DATABASE_URL: str

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    """
    ตัวแปรจาก env = ค่าจาก ไฟล์ .env = ค่าดีฟอลต์ (ถ้ามี)   
    ALGORITHM: str =  "HS256"  # ค่า "H256" คือค่า Default ถ้าไม่กำหนดใน .env (str)
    """

    class Config:
        env_file = ".env"
        extra = "ignore"  # ถ้ามีตัวแปรใน .env ที่ไม่ได้กำหนดใน Settings จะไม่เกิด error - pydantic จะละเลยตัวแปรนั้น
        # env_file_encoding = "utf-8"  # กำหนด encoding ของไฟล์ .env


settings = Settings()
