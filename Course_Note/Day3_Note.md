## FastAPI for Beginners - Day 3

### Download Trainging Document

[Click here to download the training document](https://drive.google.com/drive/folders/1jTwWio91_ckDp-9MuXP0EEYPo-TNVAVP?usp=sharing)

### Python FastAPI with PostgreSQL and ORM with SQLAlchemy

### Technology Stack
- Python 3.10+
- UV
- FastAPI
- PostgreSQL
- Asyncpg
- SQLAlchemy
- Alembic (for database migrations)
- Pydantic
- Uvicorn (ASGI server)

### System Requirements
- Python 3.10 or higher
- PostgreSQL database server
- uv
- FastAPI
- SQLAlchemy
- Asyncpg
- Alembic
- Pydantic
- Uvicorn

### โครงสร้างโปรเจ็กต์ (Project Structure)

```plaintext
fastapi-db/
├── alembic/                    # โฟลเดอร์ที่ Auto Generate มาจาก Alembic
├── app/                        # โฟลเดอร์หลักเก็บ Source Code
│   ├── __init__.py
│   ├── main.py                 # จุดเริ่มต้นของโปรแกรม (Entry Point)
│   ├── api/                    # เก็บส่วนของ API Router (URLs)
│   │   ├── __init__.py
│   │   └── v1/                 # แยก Version API (เผื่ออนาคตมี v2)
│   │       ├── __init__.py
│   │       ├── api.py          # รวม Router ทั้งหมดของ v1
│   │       └── endpoints/      # แยกไฟล์ตาม Feature (เช่น users, items)
│   │           ├── __init__.py
│   │           ├── items.py
│   │           └── users.py
│   ├── core/                   # การตั้งค่าหลักของระบบ
│   │   ├── __init__.py
│   │   ├── config.py           # โหลด Environment Variables (.env)
│   ├── db/                     # เกี่ยวกับ Database
│   │   ├── __init__.py
│   │   └── base.py             # รวม Model ทั้งหมดให้ Alembic เห็น
│   │   ├── session.py          # สร้าง Engine และ SessionLocal
│   ├── models/                 # เก็บ Database Models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── base_class.py       # Base Class สำหรับ Model
│   │   ├── item.py             # ตาราง Item
│   │   └── user.py             # ตาราง User
│   ├── schemas/                # เก็บ Pydantic Models (Request/Response)
│   │   ├── __init__.py
│   │   ├── item.py             # Schema ของ Item (Create, Response, Update)
│   │   └── user.py             # Schema ของ User (Create, Response, Update)
│   └── services/               # เก็บ Business Logic (ทำงานกับ DB)
│       ├── __init__.py
│       ├── item_service.py     # ฟังก์ชัน create_item, get_item
│       └── user_service.py     # ฟังก์ชัน create_user, get_user
├── alembic.ini                 # Config ของ Alembic
├── .env                        # เก็บความลับ (DB URL, Secret Key)
├── .env.example                # ตัวอย่างไฟล์ Config
├── .gitignore                  # ไฟล์ที่ไม่เอาขึ้น Git
├── pyproject.toml              # ไฟล์จัดการ Package ของ uv
├── README.md                   # ไฟล์เอกสารโปรเจ็กต์
└── uv.lock                     # ไฟล์ Lock version ของ uv
```

### FastAPI Authentication and Authorization with JWT

### Step 1: Install Required Packages
```bash
uv add greenlet python-jose[cryptography] bcrypt python-multipart slowapi
```
อธิบาย:
- `greenlet`: สำหรับการจัดการ context switching ใน async programming
- `python-jose[cryptography]`: สำหรับการสร้างและตรวจสอบ JWT tokens
- `bcrypt`: สำหรับการแฮชรหัสผ่าน
- `python-multipart`: สำหรับการจัดการ multipart/form-data requests
- `slowapi`: สำหรับการจำกัดอัตราการเข้าถึง (rate limiting)

### Step 2: แก้ไขไฟล์ .env เพื่อเพิ่มการตั้งค่า JWT
```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/fastapi_db
PROJECT_NAME=My FastAPI Project

# JWT Settings
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```
Generate a strong secret key using node:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

อธิบาย:
- `SECRET_KEY`: คีย์ลับที่ใช้ในการเซ็น JWT tokens ควรเป็นคีย์ที่ยาวและซับซ้อน
- `ALGORITHM`: อัลกอริทึมที่ใช้ในการเซ็น JWT tokens (เช่น HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: เวลาหมดอายุของ Access Token (หน่วย: นาที)
- `REFRESH_TOKEN_EXPIRE_DAYS`: เวลาหมดอายุของ Refresh Token (หน่วย: วัน)

### Step 3: แก้ไขไฟล์ app/core/config.py เพื่อโหลดการตั้งค่า JWT
```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # กำหนด Default ได้เฉพาะข้อมูลที่ไม่ใช่ความลับ
    PROJECT_NAME: str = "My FastAPI Project"

    # Pydantic จะบังคับให้ไปหาค่านี้จากไฟล์ .env เท่านั้น ถ้าหาไม่เจอโปรแกรมจะ Error
    DATABASE_URL: str

    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"
        extra = "ignore"
        # env_file_encoding = 'utf-8'


settings = Settings()
```

อธิบาย:
- เพิ่มการตั้งค่า JWT ในคลาส `Settings` เพื่อให้สามารถเข้าถึงค่าเหล่านี้ได้ทั่วโปรเจ็กต์ผ่าน `settings`

### Step 4: สร้างยูทิลิตี้สำหรับการจัดการ JWT tokens ในไฟล์ app/core/security.py
```python
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
import bcrypt
from app.core.config import settings


# ฟังก์ชันสำหรับสร้าง JWT Token
def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# ฟังก์ชันสำหรับสร้าง JWT Refresh Token
def create_refresh_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# ฟังก์ชันสำหรับตรวจสอบรหัสผ่าน
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# ฟังก์ชันสำหรับแฮชรหัสผ่าน
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
```

อธิบาย:
- `create_access_token`: สร้าง JWT Access Token โดยมีข้อมูล subject และเวลาหมดอายุ
- `create_refresh_token`: สร้าง JWT Refresh Token โดยมีข้อมูล subject และเวลาหมดอายุ
- `verify_password`: ตรวจสอบรหัสผ่านที่ป้อนเข้ากับรหัสผ่านที่แฮชไว้
- `get_password_hash`: แฮชรหัสผ่านโดยใช้ bcrypt


### Step 5: เพิ่มไฟล์ app/schemas/token.py สำหรับ Token Schema
```python
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    type: Optional[str] = None
```

### Step 6: แก้ไขไฟล์ app/services/user_service.py เพื่อเพิ่มฟังก์ชันการสร้างผู้ใช้พร้อมแฮชรหัสผ่าน
```python
from app.core.security import get_password_hash, verify_password

...
# ฟังก์ชันสร้างผู้ใช้ใหม่
async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)

...

async def authenticate_user(db: AsyncSession, email: str, password: str):
    if not verify_password(password, user.hashed_password):
```
โค้ดที่สมบูรณ์:
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


# ฟังก์ชัน CRUD เกี่ยวกับ User
# ฟังก์ชันดึงข้อมูลผู้ใช้ตาม ID
async def get_user(db: AsyncSession, user_id: int):
    # ใช้ select() แทน query()
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


# ฟังก์ชันดึงข้อมูลผู้ใช้ตาม email
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


# ฟังก์ชันดึงรายชื่อผู้ใช้ทั้งหมด (มีการข้ามและจำกัดจำนวน)
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


# ฟังก์ชันสร้างผู้ใช้ใหม่
async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    await db.commit()  # ต้อง await ตอน commit
    await db.refresh(db_user)  # ต้อง await ตอน refresh
    return db_user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
```

### Step 7: สร้าง Endpoint สำหรับการ auth ในไฟล์ app/api/v1/endpoints/auth.py
```python
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.user import User, UserCreate
from app.services import user_service

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    request: Request,
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = await user_service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/register", response_model=User)
async def register_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    user = await user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await user_service.create_user(db, user=user_in)
    return user


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    refresh_token: str,
) -> Any:
    # In a real application, you should verify the refresh token and check if it's in the database or blacklist
    # For simplicity, we just decode it and create a new access token
    try:
        payload = security.jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            token_data, expires_delta=access_token_expires
        ),
        "refresh_token": refresh_token,  # Return the same refresh token or rotate it
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}
```

### Step 8: แก้ไขไฟล์ app/api/deps.py เพื่อเพิ่ม Dependency สำหรับการเชื่อมต่อฐานข้อมูล
```python
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import config
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload
from app.services import user_service

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/auth/login"
)


# เปลี่ยนจาก Generator ธรรมดา เป็น AsyncGenerator
async def get_db() -> AsyncGenerator:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            # SessionLocal จะปิดตัวเองอัตโนมัติเมื่อจบ async with
            # หรือถ้าไม่ได้ใช้ context manager ต้อง await db.close() เอง
            pass


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await user_service.get_user(db, user_id=int(token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### Step 9: แก้ไขไฟล์ app/api/v1/api.py เพื่อเพิ่ม Router ของ Auth
```python
from fastapi import APIRouter, Depends
from app.api import deps
from app.api.v1.endpoints import users, items, auth

# สร้าง API Router หลัก
api_router = APIRouter()

# รวม Route ของ Auth
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# รวม Route ของ Users (Protected)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(deps.get_current_active_user)]
)

# รวม Route ของ Items (Protected)
api_router.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(deps.get_current_active_user)]
)
```

### Step 10: รันแอปพลิเคชัน FastAPI
ใช้คำสั่งต่อไปนี้เพื่อรันแอปพลิเคชัน FastAPI
```bash
uv run uvicorn app.main:app --reload
```

#### 10.1 ทดสอบ API
- เปิดเบราว์เซอร์และไปที่ `http://localhost:8000/` เพื่อดูข้อความต้อนรับ
- ไปที่ `http://localhost:8000/scalar` เพื่อดู Scalar API Documentation


### Step 11: ทดสอบการทำงานของ Authentication
- ใช้เครื่องมือเช่น Postman หรือ curl เพื่อทดสอบการลงทะเบียนผู้ใช้, การเข้าสู่ระบบ, และการรีเฟรชโทเค็น
- ตรวจสอบว่า Endpoints ที่ต้องการการยืนยันตัวตนสามารถเข้าถึงได้เฉพาะเมื่อมีโทเค็นที่ถูกต้องเท่านั้น

### Step 12: เพิ่ม Rate Limiting ด้วย SlowAPI
#### Step 12.1: สร้างไฟล์ app/core/limiter.py
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

# สร้าง Limiter instance
# key_func=get_remote_address หมายถึงจะจำกัดการเรียกใช้งานโดยดูจาก IP Address ของผู้เรียก
limiter = Limiter(key_func=get_remote_address)
```

#### Step 12.2: แก้ไขไฟล์ app/api/v1/endpoints/auth.py เพื่อเพิ่ม Rate Limiting
```python

from app.core.limiter import limiter

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")  # จำกัดการเรียกใช้งาน 5 ครั้งต่อนาที
async def login_access_token(
    request: Request,  # จำเป็นต้องรับ Request เข้ามาเพื่อให้ Limiter ทำงาน
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:

... (rest of the code remains unchanged) ...
```

#### Step 12.3: แก้ไขไฟล์ app/main.py เพื่อเพิ่ม Middleware ของ SlowAPI
```python
# นำเข้า FastAPI จากไลบรารี fastapi
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# นำเข้า api_router ที่เราสร้างไว้ใน api/v1/api.py
from app.api.v1.api import api_router
from app.core.limiter import limiter

# สำหรับ Scalar API reference
from scalar_fastapi import get_scalar_api_reference

# สร้างแอปพลิเคชัน FastAPI
app = FastAPI(title="My FastAPI App")

# ตั้งค่า Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


# นำ Router ทั้งหมดมาแปะที่ /api/v1
app.include_router(api_router, prefix="/api/v1")


# เส้นทาง API สำหรับดู Scalar API reference
# Path: /scalar
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        # title="Scalar FastAPI API Reference",
        title=app.title,
    )
```

#### Step 12.4: ทดสอบ Rate Limiting
- ใช้ Postman หรือ curl เพื่อทดสอบการเรียกใช้งาน Endpoint `/api/v1/auth/login` เกิน 5 ครั้งภายใน 1 นาที
- คุณควรได้รับข้อความแจ้งเตือนว่ามีการเรียกใช้งานเกินอัตราที่กำหนด
- ตัวอย่างข้อความแจ้งเตือน:
```json
{
  "detail": "Rate limit exceeded: 5 per 1 minute"
}
```

### Step 13. การเขียน Dockerfile และ docker-compose.yml สำหรับรันแอปพลิเคชัน FastAPI กับ PostgreSQL

#### Step 13.1 เขียน Dockerfile
```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the project configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures we use the exact versions from uv.lock
RUN uv sync --frozen

# Copy the rest of the application code
COPY . .

# Add the virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 13.2 เขียน docker-compose.yml
```yaml
networks:
  fastapi-db-network:
    name: fastapi-db-network
    driver: bridge

services:
  db:
    image: postgres:17
    container_name: fastapi-db-postgres
    restart: always
    environment:
      POSTGRES_USER: "${POSTGRES_USER}"
      POSTGRES_PASSWORD: "${POSTGRES_PASSWORD}"
      POSTGRES_DB: "${POSTGRES_DB}"
    ports:
      - "${POSTGRES_PORT}:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - fastapi-db-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    container_name: fastapi-db-web
    restart: always
    ports:
      - "8000:8000"
    environment:
      # Use the service name 'db' as the hostname
      DATABASE_URL: "postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
    depends_on:
      db:
        condition: service_healthy
    networks: 
      - fastapi-db-network
    # Optional: Run migrations automatically on startup
    command: sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"

volumes:
  db_data:
```

#### Step 13.3 สร้างไฟล์ .env สำหรับ Docker Compose
สร้างไฟล์ `.env` ในโฟลเดอร์เดียวกับ `docker-compose.yml`
```env
PROJECT_NAME=My FastAPI Project

# Database Configuration (Used by Docker Compose)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=fastapi_db
POSTGRES_PORT=5532

# Database URL for Local Development
# Note: When running in Docker, this is overridden by docker-compose.yml
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/fastapi_db

# JWT Settings
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### Step 13.4 รันแอปพลิเคชันด้วย Docker Compose
ใช้คำสั่งต่อไปนี้เพื่อรันแอปพลิเคชันด้วย Docker Compose
```bash
docker compose up -d --build
```

#### Step 13.5 ทดสอบแอปพลิเคชัน
- เปิดเบราว์เซอร์และไปที่ `http://localhost:8000/` เพื่อดูข้อความต้อนรับ
- ไปที่ `http://localhost:8000/scalar` เพื่อดู Scalar API Documentation
