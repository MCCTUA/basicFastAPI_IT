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
    # (**item.model_dump()) ** เรียกว่า Dictionary Unpacking จะเป็นการแตก dictionary ออกมาเป็น argument เช่น title = item.title, description = item.description คล้ายๆ กับ javascript spread operator(...item, owner_id=user_id)
    db_item = Item(**item.model_dump(), owner_id=user_id)

    db.add(db_item)
    await db.commit()  # รอ commit
    await db.refresh(db_item)  # รอ refresh ข้อมูลกลับมา (เช่น id ที่ auto-gen)
    return db_item


# เพิ่มฟังก์ชันอื่นๆ ตามต้องการ (update, delete)
