from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.schemas.user import UserCreate, UserResponse, UserUpdate
from services import user_service

router = APIRouter()

@router.get("/", response_model=UserResponse)
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_service.get_multi(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(id: int, db: AssertionError = Depends(get_db)):
    user = await user_service.get(db, id=int(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user 

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    current_user = await user_service.get_by_email(db, email=user.email)

    if current_user:
        raise HTTPException(status_code=400, detail="Email aleardy registered")
    return await user_service.create(db=db, obj_in=user)

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="user update"
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    # 1. ดึงข้อมูล User เดิมออกมาจาก DB
    user = await user_service.get(db, id=int(user_id))
    # 2. ตรวจสอบว่ามี User คนนี้ไหม (แก้ไขข้อความ Error ให้ตรงบริบทด้วยครับ)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 3. 
    return await user_service.update(
        db=db, 
        db_obj=user, # <--- ต้องส่งก้อนข้อมูล (Instance) ที่ดึงมาจาก DB เข้าไป
        obj_in=data
        )

@router.delete(
    "/{user_id}", 
    response_model=UserResponse,
    summary="delete user"
    )
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    user = await user_service.get(db, id=int(user_id))
    print(f"user is {user}")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_service.remove(db=db, id=int(user_id))