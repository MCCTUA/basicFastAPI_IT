from typing import List
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from src.db.base import Base

class Users(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True
        )
    username : Mapped[str] = mapped_column(
        String(128), 
        nullable=False
        )
    first_name : Mapped[str] = mapped_column(
        String(128), 
        nullable=False
        )
    last_name : Mapped[str] = mapped_column(
        String(128), 
        nullable=False
        )
    email : Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False
        )
    hashed_password : Mapped[str] = mapped_column(
        String, 
        nullable=False
        )
    is_active : Mapped[bool] = mapped_column(
        Boolean, 
        default=True
        )
    # Relationship: เชื่อมไปหา Product
    # - back_populates: ต้องตรงกับชื่อตัวแปรใน Product Model
    # - cascade: ห้ามใส่ "all, delete" เด็ดขาด เพื่อไม่ให้ลบสินค้าตาม user
    # Syntax :- products : Mapped[Class_Name] = relationship(back_populates="field_name")
    # field_name คือ field ใน Products Table ที่อ้างกลับมาที่ Users 
    products: Mapped[List["Products"]] = relationship(back_populates="creator")
