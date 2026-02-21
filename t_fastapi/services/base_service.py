from typing import Generic, TypeVar, Type, Optional, List, Any, Union, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseService(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]): # model มี type hind เป็น Type[ModelType]
        """
        Base class สำหรับ CRUD
        :param model: SQLAlchemy model class (เช่น Users, Products)
        """
        self.model = model
    #------------------------
    # Method get By Id
    #------------------------
    # db: AsyncSession สื่อสารกับ DB ผ่าน Session แบบ Asynchronous
    # -> Optional[ModelType] จะ return เป็น [ModelTyp] ก็ได้ หรือไม่ Return ก็ได้ เนื่องจากเป็น Optional
    async def get(self, db: AsyncSession, id: str | int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()
    
    #------------------------
    # Method get multi items
    #------------------------
    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    #------------------------
    # Method create item
    #------------------------
    async def create(self, db: AsyncSession, *, obj_in: Any) -> ModelType:
        # 1. ลองทำรายการ (ขับรถข้ามสะพาน)
        try:
            """
            แปลง Pydantic Schema (จาก Frontend) ให้เป็น SQLAlchemy Model/q
            """
            data = self.model(**obj_in.model_dump())
            # นำข้อมูล (data) ไปรอใน Que ของ Database Session บอก SQLAlchemy ให้เตรียมตัวเอาข้อมูลไปเพิ่มในตาราง
            db.add(data)
            # เหมือนกับการกด save data ลงฐานข้อมูล
            await db.commit()
            # เมื่อกด save แล้ว ฐานข้อมูลจะจัดการข้อมูลบ่้างส่วนเอง เช่น สร้าง id, createAt, updateAt เราจึงต้อง refresh ข้อมูลก่อน เพื่อเอา ข้อมูลเหล่านี้ไม่เช่นนั้นจะได้ค่า None หรือ Error ตอนส่งกลับไปหา Frontend
            await db.refresh(data)
            # เพื่อส่งข้อมูลไปบอก Frontend ว่า บันทึกสำเร็จหรือไม่
            return data

        # 2. ถ้าพัง (ตกเหว)
        except Exception as e:
            await db.rollback()
            raise e

        # 3. ไม่ว่าจะรอดหรือพัง (จุดเช็กชื่อ)
        finally:
            # ปกติ FastAPI จะปิด session ให้เราอยู่แล้ว แต่ถ้าเขียน script แยก
            # เรามักจะสั่งปิดการเชื่อมต่อที่นี่
            pass

    #------------------------
    # Update (รองรับทั้ง PUT และ PATCH)
    #------------------------

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[Any, Dict[str, Any]]
    ) -> ModelType:
        try:
            # 1. แปลงข้อมูล Pydantic เป็น Dict
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                # exclude_unset=True สำคัญมากสำหรับการทำ PATCH (อัปเดตบางฟิลด์)
                update_data = obj_in.model_dump(exclude_unset=True)

            # 2. ใช้ setattr เพื่ออัปเดตค่าแบบ Dynamic
            for field in update_data:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, update_data[field])

            # 3. บันทึกข้อมูล
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj

        except Exception as e:
            # เมื่อพัง ต้องถอยกลับ (Rollback)
            await db.rollback()
            raise e
            
        finally:
            # ทำงานเสมอ (ในที่นี้ปล่อยว่างไว้ได้)
            pass

    #------------------------
    #  Delete
    #------------------------
    async def remove(
        self, 
        db: AsyncSession,
        *,
        id: str | int
        ) -> Optional[ModelType]:
        try:
            obj = await self.get(db, id)
            if obj:
                await db.delete(obj)
                await db.commit()
            return obj
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            pass