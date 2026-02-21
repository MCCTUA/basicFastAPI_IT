from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True
        )
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column( Text )
    price: Mapped[float] = mapped_column( Float )
    stock: Mapped[int] = mapped_column(Integer, default = 0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # CreatedBy Attributes:
    # 1. nullable=True: สำคัญมาก! เพื่อให้เมื่อ User ถูกลบ ฟิลด์นี้กลายเป็น NULL ได้
    # 2. ondelete="SET NULL": คำสั่งในระดับฐานข้อมูล บอกว่าถ้า User ตาย ให้เซตช่องนี้เป็นว่าง
    # ForeignKey Syntax : mapped_column(ForeignKey("ชื่อตาราง.ชื่อคอลัมน์"))
    created_by_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    # Relationship: เชื่อมกลับไปหา User
    creator: Mapped[Optional["Users"]] = relationship(back_populates="products")