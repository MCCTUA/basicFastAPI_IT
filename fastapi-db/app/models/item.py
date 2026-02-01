from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_class import Base


class Item(Base):
    __tablename__ = "items"  # ชื่อตารางในฐานข้อมูล

    id = Column(Integer, primary_key=True, index=True)  # รหัสสินค้า
    title = Column(String(255), index=True)  # ชื่อสินค้า
    description = Column(String, nullable=True)  # คำอธิบายสินค้า

    # ForeignKey: ผูกกับตาราง users คอลัมน์ id
    owner_id = Column(Integer, ForeignKey("users.id"))

    # ความสัมพันธ์: Item นี้เป็นของ User คนไหน
    # back_populates จะชี้ไปที่ตัวแปร 'items' ในไฟล์ User ความสัมพันธ์ที่ดีควรจะเชื่อมโยงกันทั้งสองฝั่ง ใน Item มี owner ชี้ไปที่ User และใน User มี items ชี้ไปที่ Item
    owner = relationship("User", back_populates="items")
