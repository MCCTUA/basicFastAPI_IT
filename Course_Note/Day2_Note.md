## FastAPI for Beginners - Day 2

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

### Step 1: สร้างฐานข้อมูล PostgreSQL
1. ติดตั้ง PostgreSQL บนเครื่องของคุณ
2. สร้างฐานข้อมูลใหม่สำหรับโปรเจค FastAPI ของคุณ
   ```sql
   CREATE DATABASE fastapi_db;
   ```
3. สร้างผู้ใช้ใหม่และกำหนดสิทธิ์ให้กับฐานข้อมูล
   ```sql
   CREATE USER fastapi_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
   ```

### Step 2: สร้างโปรเจ็กต์ FastAPI ด้วย UV
1. คำสั่งสร้างโปรเจ็กต์ FastAPI
   ```bash
   uv init --python 3.13 fastapi-db
   ```

2. เข้าไปในโฟลเดอร์โปรเจ็กต์
   ```bash
   cd fastapi-db
   ```

3. ติดตั้งไลบรารีที่จำเป็น
   ```bash
   uv add fastapi uvicorn sqlalchemy asyncpg alembic pydantic pydantic[email] pydantic-settings cryptography scalar-fastapi
    ```
อธิบายแพ็กเกจที่ติดตั้ง:
    - `fastapi`: Framework สำหรับสร้าง API
    - `uvicorn`: ASGI server สำหรับรันแอปพลิเคชัน FastAPI
    - `sqlalchemy`: ORM สำหรับจัดการฐานข้อมูล
    - `asyncpg`: ไลบรารีสำหรับเชื่อมต่อกับ PostgreSQL แบบอะซิงโครนัส
    - `alembic`: เครื่องมือสำหรับจัดการการเปลี่ยนแปลงโครงสร้างฐานข้อมูล (migrations)
    - `pydantic`: ไลบรารีสำหรับการตรวจสอบและจัดการข้อมูล
    - `pydantic[email]`: ส่วนขยายของ Pydantic สำหรับการตรวจสอบอีเมล
    - `pydantic-settings`: ส่วนขยายของ Pydantic สำหรับการจัดการการตั้งค่า อ่านค่าจาก environment variables
    - `cryptography`: ไลบรารีสำหรับการเข้ารหัสข้อมูล
    - `scalar-fastapi`: เครื่องมือเสริมสำหรับ FastAPI


### Step 3: สร้างโครงสร้างโปรเจ็กต์
สร้างโฟลเดอร์และไฟล์ต่าง ๆ สำหรับโปรเจ็กต์ของคุณ
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
├── .env.example                # เก็บความลับ (DB URL, Secret Key)
├── .gitignore                  # ไฟล์ที่ไม่เอาขึ้น Git
├── pyproject.toml              # ไฟล์จัดการ Package ของ uv
├── README.md                   # ไฟล์เอกสารโปรเจ็กต์
└── uv.lock                     # ไฟล์ Lock version ของ uv
```

### Step 4: ทดสอบ การรันแอปพลิเคชัน FastAPI และ Scalar API Documentation
#### 4.1 สร้างไฟล์ `app/main.py`
```python
# นำเข้า FastAPI จากไลบรารี fastapi
from fastapi import FastAPI

# สำหรับ Scalar API reference
from scalar_fastapi import get_scalar_api_reference

# สร้างแอปพลิเคชัน FastAPI
app = FastAPI()


# สร้างเส้นทาง (route) สำหรับ root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI with uv!"}


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

#### 4.2 รันแอปพลิเคชัน FastAPI
ใช้คำสั่งต่อไปนี้เพื่อรันแอปพลิเคชัน FastAPI
```bash
uv run uvicorn app.main:app --reload
```

#### 4.3 ทดสอบ API
- เปิดเบราว์เซอร์และไปที่ `http://localhost:8000/` เพื่อดูข้อความต้อนรับ
- ไปที่ `http://localhost:8000/scalar` เพื่อดู Scalar API Documentation

### Step 5: ตั้งค่า Database Connection
#### 5.1 สร้างไฟล์ `.env` สำหรับเก็บค่าการตั้งค่าฐานข้อมูล ไว้ในโฟลเดอร์ root (นอกสุด) ของโปรเจ็กต์
```.env
# .env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/fastapi_db
PROJECT_NAME=My FastAPI Project
```

#### 5.2 สร้างไฟล์ `app/core/config.py` สำหรับโหลดค่าการตั้งค่า
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # กำหนด Default ได้เฉพาะข้อมูลที่ไม่ใช่ความลับ
    PROJECT_NAME: str = "My FastAPI Project"
    
    # Pydantic จะบังคับให้ไปหาค่านี้จากไฟล์ .env เท่านั้น ถ้าหาไม่เจอโปรแกรมจะ Error
    DATABASE_URL: str 

    class Config:
        env_file = ".env"
        # env_file_encoding = 'utf-8'

settings = Settings()
```

### Step 6: สร้างไฟล์ Engine และ Session สำหรับเชื่อมต่อฐานข้อมูล
#### 6.1 สร้างไฟล์ `app/db/session.py`
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# 1. สร้าง Async Engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 2. สร้าง Session Factory
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# 3. Dependency สำหรับใช้ใน API Endpoint (Dependency Injection)
async def get_db():
    async with SessionLocal() as session:
        yield session
```

### Step 7: สร้าง Base Model สำหรับ ORM (พระเอกของ SQLAlchemy)
#### 7.1 สร้างไฟล์ `app/models/base_class.py`
```python
from sqlalchemy.orm import DeclarativeBase


# สร้าง Base Class ก่อน เพื่อให้ทุก Model สืบทอดมาจากตัวนี้
class Base(DeclarativeBase):
    pass
```

### Step 8: สร้าง Model ตัวอย่าง User และ Item
#### 8.1 สร้างไฟล์ `app/models/user.py`
```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base_class import Base

class User(Base):
    __tablename__ = "users" # ชื่อตารางในฐานข้อมูล

    # คอลัมน์ต่างๆ ในตาราง users
    # id, email, hashed_password, is_active, first_name, last_name
    # String(255) กำหนดความยาวสูงสุดของสตริง
    # String ไม่ได้กำหนดความยาวสูงสุดจึงใช้สำหรับข้อมูลที่ยาวไม่จำกัด
    id = Column(Integer, primary_key=True, index=True) # รหัสผู้ใช้
    first_name = Column(String(128), nullable=False) # ชื่อจริง
    last_name = Column(String(128), nullable=False) # นามสกุล
    email = Column(String(255), unique=True, index=True, nullable=False) # อีเมล
    hashed_password = Column(String, nullable=False) # รหัสผ่านที่ถูกเข้ารหัส
    is_active = Column(Boolean, default=True) # สถานะผู้ใช้ (เปิดใช้งานหรือไม่)

    # ความสัมพันธ์: 1 User มีหลาย Items
    # back_populates จะชี้ไปที่ตัวแปร 'owner' ในไฟล์ Item
    # cascade="all, delete-orphan" หมายความว่า ถ้า User ถูกลบ Items ที่เกี่ยวข้องจะถูกลบด้วย
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")
```
#### 8.2 สร้างไฟล์ `app/models/item.py`
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_class import Base

class Item(Base):
    __tablename__ = "items" # ชื่อตารางในฐานข้อมูล

    id = Column(Integer, primary_key=True, index=True) # รหัสสินค้า
    title = Column(String(255), index=True) # ชื่อสินค้า
    description = Column(String, nullable=True) # คำอธิบายสินค้า
    
    # ForeignKey: ผูกกับตาราง users คอลัมน์ id
    owner_id = Column(Integer, ForeignKey("users.id"))

    # ความสัมพันธ์: Item นี้เป็นของ User คนไหน
    # back_populates จะชี้ไปที่ตัวแปร 'items' ในไฟล์ User
    owner = relationship("User", back_populates="items")
```

### Step 9: ตัรวม Model ให้ Alembic มองเห็น
#### 9.1 สร้างไฟล์ `app/db/base.py`
```python
# Import Base มาก่อน
from app.models.base_class import Base

# Import Models ทั้งหมดที่อยากให้สร้างตาราง
from app.models.user import User
from app.models.item import Item

# สรุป: ไฟล์นี้มีหน้าที่รวมญาติ เพื่อให้ Alembic import ไปใช้ที่เดียวจบ
# โดยไม่ต้องไปไล่ import ทีละไฟล์ model
```

### Step 10: การตั้งค่า Alembic (Migration)
#### 10.1 เริ่มต้น Alembic (แบบ Async)
```bash
alembic init -t async alembic
```

#### 10.2 แก้ไขไฟล์ `alembic/env.py` เพื่อเชื่อมต่อกับฐานข้อมูลและ Model ของเรา
```python

from alembic import context

# ----------------- [จุดที่แก้ 1] Import ของเราเข้ามา -----------------
from app.core.config import settings  # 1. เอา URL จาก Config เรา
from app.db.base import Base  # 2. เอา Base ที่รวม Model แล้วมา
# -------------------------------------------------------------------

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# ----------------- [จุดที่แก้ 2] ตั้งค่า URL -----------------
# ให้ Alembic ใช้ URL จาก pydantic-settings ของเรา แทนที่ใน alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
# -------------------------------------------------------------------

# ----------------- [จุดที่แก้ 3] บอก Target Metadata -----------------
target_metadata = Base.metadata  # เพื่อให้มันเทียบ Model กับ Database จริง
# -------------------------------------------------------------------
```

### Step 11: สร้าง Migration Script และอัพเดตฐานข้อมูล
#### 11.1 สร้าง Migration File (Revision): คำสั่งนี้จะไปอ่านไฟล์ Python เทียบกับ Database แล้วสร้างไฟล์ script สำหรับสร้างตาราง
```bash
alembic revision --autogenerate -m "Init users and items tables"
```
> ถ้าสำเร็จ: จะมีไฟล์ใหม่โผล่มาในโฟลเดอร์ alembic/versions/xxxx_init...py ลองเปิดดูจะเห็นคำสั่ง create_table

#### 11.2 อัปเดต Database (Upgrade): คำสั่งนี้จะรันไฟล์ script เพื่อสร้างตารางใน Database จริง
```bash
alembic upgrade head
```
> ตรวจสอบ Database: ลองใช้โปรแกรมเปิด Database ดู (เช่น DBeaver หรือ pgAdmin) จะเห็นตาราง users และ items ถูกสร้างขึ้นมาเรียบร้อยแล้ว

### Troubleshooting
หากคุณต้องการเริ่มต้นระบบ Migration ใหม่ทั้งหมด (Reset Migration) เพื่อให้เหมือนกับเพิ่งเริ่มโปรเจ็กต์ สามารถทำตามขั้นตอนที่ผมเพิ่งทำให้ได้เลย

1. ล้างข้อมูลใน Database (Downgrade): สั่งให้ Alembic ย้อนกลับการเปลี่ยนแปลงทั้งหมดเพื่อลบตารางเก่าออก
   ```bash
   alembic downgrade base
   ```
2. ลบไฟล์ Migration เก่า: ลบไฟล์ `.py` ในโฟลเดอร์ `versions` ทิ้งให้หมด
    ```
    # Windows PowerShell
    Remove-Item alembic\versions\*.py

    # CMD
    del alembic\versions\*.py

    # Linux / macOS
    rm -rf alembic/versions/*.py
    ```
3. สร้างไฟล์ Migration ใหม่: สั่งให้ Alembic สร้างไฟล์ Migration ใหม่ตามโครงสร้างปัจจุบันของโมเดล
   ```bash
   alembic revision --autogenerate -m "Init users and items tables"
   ```
4. อัปเดต Database ใหม่: สั่งให้ Alembic รันไฟล์ Migration ใหม่เพื่อสร้างตาราง
   ```bash
    alembic upgrade head
    ```

### Step 12: สร้าง CRUD Operations สำหรับ User และ Item
#### 12.1 Schemas (Pydantic Models) สำหรับ User และ Item
##### 12.1.1 สร้างไฟล์ `app/schemas/user.py`
```python
from typing import Optional
from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Properties to return via API
class User(UserBase):
    id: int

    class Config:
        from_attributes = True # รองรับ ORM mode (v2 ใช้ config นี้)
```

##### 12.1.2 สร้างไฟล์ `app/schemas/item.py`
```python
from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ItemCreate(ItemBase):
    title: str

class ItemUpdate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True # รองรับ ORM mode (v2 ใช้ config นี้)
```

### Step 13: สร้าง Service (Business Logic) Layer สำหรับ User และ Item
ส่วนนี้จะคุยกับ Database ผ่าน SQLAlchemy Session ตัด Logic ออกจาก Router
#### 13.1 สร้างไฟล์ `app/services/user_service.py`
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate

# สมมติว่ามีฟังก์ชัน hash password ใน core/security.py
# from app.core.security import get_password_hash


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
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(
        email=user.email, 
        hashed_password=fake_hashed_password, 
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    await db.commit()  # ต้อง await ตอน commit
    await db.refresh(db_user)  # ต้อง await ตอน refresh
    return db_user
# เพิ่มฟังก์ชันอื่นๆ ตามต้องการ (update, delete)
```

#### 13.2 สร้างไฟล์ `app/services/item_service.py`
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.item import Item
from app.schemas.item import ItemCreate


# ฟังก์ชัน CRUD เกี่ยวกับ Item
# ฟังก์ชันดึงข้อมูลไอเท็มตาม ID
async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    # ใช้ select() และ await db.execute()
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return result.scalars().all()


# ฟังก์ชันสร้างไอเท็มใหม่
async def create_user_item(db: AsyncSession, item: ItemCreate, user_id: int):
    # Pydantic v2 ใช้ model_dump(), ถ้า v1 ใช้ dict()
    # สร้าง Object Item โดยผูกกับ user_id
    db_item = Item(**item.model_dump(), owner_id=user_id)

    db.add(db_item)
    await db.commit()  # รอ commit
    await db.refresh(db_item)  # รอ refresh ข้อมูลกลับมา (เช่น id ที่ auto-gen)
    return db_item
# เพิ่มฟังก์ชันอื่นๆ ตามต้องการ (update, delete)
```

### Step 14: สร้าง API Endpoints สำหรับ User และ Item
ส่วนรับ Request จาก Client และเรียกใช้ Service
Utility: สร้าง Dependency สำหรับรับ DB Session (อยู่ใน app/api/deps.py)
#### 14.1 สร้างไฟล์ `app/api/deps.py`
```python
from typing import AsyncGenerator
from app.db.session import SessionLocal

# เปลี่ยนจาก Generator ธรรมดา เป็น AsyncGenerator
async def get_db() -> AsyncGenerator:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            # SessionLocal จะปิดตัวเองอัตโนมัติเมื่อจบ async with
            # หรือถ้าไม่ได้ใช้ context manager ต้อง await db.close() เอง
            pass
```
#### 14.2 แก้ไขไฟล์ `app/api/v1/endpoints/users.py` เพื่อใช้ AsyncSession และ await
```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  # เปลี่ยน import เป็น AsyncSession

from app.api import deps  # หรือตำแหน่งที่คุณเก็บ get_db
from app.schemas import user as user_schema
from app.services import user_service

# สร้าง Router สำหรับ User Endpoints
router = APIRouter()


# Endpoint ดึงรายชื่อผู้ใช้ทั้งหมด
@router.get("/", response_model=List[user_schema.User])
async def read_users(  # เพิ่ม async
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db),  # เปลี่ยน Type hint
):
    # เพิ่ม await
    users = await user_service.get_users(db, skip=skip, limit=limit)
    return users


# Endpoint สร้างผู้ใช้ใหม่
@router.post("/", response_model=user_schema.User)
async def create_user(  # เพิ่ม async
    user: user_schema.UserCreate, db: AsyncSession = Depends(deps.get_db)
):
    # เพิ่ม await
    db_user = await user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_service.create_user(db=db, user=user)


# Endpoint ดึงข้อมูลผู้ใช้ตาม ID
@router.get("/{user_id}", response_model=user_schema.User)
async def read_user(user_id: int, db: AsyncSession = Depends(deps.get_db)):  # เพิ่ม async
    # เพิ่ม await
    db_user = await user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```
#### 14.3 แก้ไขไฟล์ `app/api/v1/endpoints/items.py` เพื่อใช้ AsyncSession และ await
```python
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas import item as item_schema
from app.services import item_service

# สร้าง Router สำหรับ Item Endpoints
router = APIRouter()


# Endpoint ดึงรายชื่อไอเท็มทั้งหมด
@router.get("/", response_model=List[item_schema.Item])
async def read_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(deps.get_db)
):
    # เพิ่ม await
    items = await item_service.get_items(db, skip=skip, limit=limit)
    return items


# Endpoint สร้างไอเท็มใหม่สำหรับผู้ใช้
@router.post("/{user_id}/items/", response_model=item_schema.Item)
async def create_item_for_user(
    user_id: int, item: item_schema.ItemCreate, db: AsyncSession = Depends(deps.get_db)
):
    # เพิ่ม await
    return await item_service.create_user_item(db=db, item=item, user_id=user_id)
```

### Step 15: Wiring (รวม Router)
ขั้นตอนสุดท้ายคือรวมทุก Endpoints เข้าด้วยกันที่ api.py
**ไฟล์:** `app/api/v1/api.py`
```python
from fastapi import APIRouter
from app.api.v1.endpoints import users, items

# สร้าง API Router หลัก
api_router = APIRouter()

# รวม Route ของ Users
api_router.include_router(users.router, prefix="/users", tags=["users"])

# รวม Route ของ Items
api_router.include_router(items.router, prefix="/items", tags=["items"])
```

**ไฟล์:** app/main.py
```python
# นำเข้า FastAPI จากไลบรารี fastapi
from fastapi import FastAPI

# นำเข้า api_router ที่เราสร้างไว้ใน api/v1/api.py
from app.api.v1.api import api_router

# สำหรับ Scalar API reference
from scalar_fastapi import get_scalar_api_reference

# สร้างแอปพลิเคชัน FastAPI
app = FastAPI(title="My FastAPI App")


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

### Step 16: ทดสอบ API Endpoints
รันแอปพลิเคชัน FastAPI
```bash
uv run uvicorn app.main:app --reload
```

ทดสอบ API Endpoints ผ่านทางเบราว์เซอร์หรือ Postman
- ดูเอกสาร API ที่ `http://localhost:8000/scalar`
- ทดสอบ User Endpoints ที่ `http://localhost:8000/api/v1/users`
- ทดสอบ Item Endpoints ที่ `http://localhost:8000/api/v1/items`