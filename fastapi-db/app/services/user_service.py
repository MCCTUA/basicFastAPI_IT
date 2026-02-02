from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


# สมมติว่ามีฟังก์ชัน hash password ใน core/security.py
# from app.core.security import get_password_hash


# ฟังก์ชัน CRUD เกี่ยวกับ User
# ฟังก์ชันดึงข้อมูลผู้ใช้ตาม ID
async def get_user(db: AsyncSession, user_id: int):
    # ใช้ select() แทน query()
    result = await db.execute(select(User).filter(User.id == user_id))
    # scalars() ไม่ใช้ scalar ที่ทำเอกสาร แต่หมายถึง ดึงผลลัพธ์เป็น scalar values
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
        last_name=user.last_name,
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


# ฟังก์ชันอัพเดตข้อมูลผู้ใช้
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        db_user.email = user_update.email
        db_user.hashed_password = user_update.password + "notreallyhashed"
        db_user.first_name = user_update.first_name
        db_user.last_name = user_update.last_name
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    return db_user


# ฟังก์ชันลบผู้ใช้
async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
