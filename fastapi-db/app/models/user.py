# column, Integer, String, Boolean มาจาก SQLAlchemy ใช้สำหรับกำหนดชนิดข้อมูลของคอลัมน์ในตาราง
from sqlalchemy import Column, Integer, String, Boolean

# relationship มาจาก SQLAlchemy ORM ใช้สำหรับกำหนดความสัมพันธ์ระหว่างตาราง
from sqlalchemy.orm import relationship

# base class มาจาก base_class.py เรา import Base มาใช้เป็นแม่แบบของ Model นี้
from .base_class import Base


class User(Base):
    __tablename__ = (
        "users"  # ชื่อตารางในฐานข้อมูล ถ้าไม่กำหนดบรรทัดนี้ SQLAlchemy จะใช้ชื่อตัวแปร class แทน
    )

    # คอลัมน์ต่างๆ ในตาราง users
    # id, email, hashed_password, is_active, first_name, last_name
    # String(255) กำหนดความยาวสูงสุดของสตริง
    # String ไม่ได้กำหนดความยาวสูงสุดจึงใช้สำหรับข้อมูลที่ยาวไม่จำกัด
    """
    Integer: ใช้สำหรับเก็บตัวเลขจำนวนเต็ม เช่น id
    String: ใช้สำหรับเก็บข้อความ เช่น ชื่อ, อีเมล
    Boolean: ใช้สำหรับเก็บค่าจริง/เท็จ เช่น is_active
    Index: การสร้างดัชนีช่วยเพิ่มประสิทธิภาพในการค้นหาข้อมูลในคอลัมน์นั้น ๆ ทำให้การค้นหาข้อมูลเร็วขึ้น
    Primary Key: คอลัมน์ที่เป็น primary key จะมีค่าที่ไม่ซ้ำกันในแต่ละแถว และใช้ในการระบุแถวข้อมูลอย่างเฉพาะเจาะจง
    Unique: การกำหนด unique ให้กับคอลัมน์จะทำให้ค่าที่ถูกเก็บในคอลัมน์นั้นไม่ซ้ำกันในแต่ละแถว
    Nullable: การกำหนด nullable=False หมายความว่าคอลัมน์นั้นต้องมีค่าเสมอ ไม่สามารถปล่อยว่างได้
    """
    id = Column(Integer, primary_key=True, index=True)  # รหัสผู้ใช้
    first_name = Column(String(128), nullable=False)  # ชื่อจริง
    last_name = Column(String(128), nullable=False)  # นามสกุล
    email = Column(String(255), unique=True, index=True, nullable=False)  # อีเมล
    hashed_password = Column(String, nullable=False)  # รหัสผ่านที่ถูกเข้ารหัส
    is_active = Column(Boolean, default=True)  # สถานะผู้ใช้ (เปิดใช้งานหรือไม่)

    # ความสัมพันธ์: 1 User มีหลาย Items (1 to Many)
    # Item คือ ชื่อตัวแปร relationship ที่เชื่อมกับ Model Item เป็นชื่อเดียวกับ Class Item ในไฟล์ item.py
    # back_populates คือ ชื่อตัวแปร relationship ที่เชื่อมกับ Model User ในไฟล์ item.py โดยใช้ 'owner' เป็นตัวเชื่อมกลับมาที่ User
    # cascade="all, delete-orphan" หมายความว่า ถ้า User ถูกลบ Items ที่เกี่ยวข้องจะถูกลบด้วย และ all หมายถึงการทำงานทุกอย่างที่เกี่ยวข้องกับความสัมพันธ์นี้จะถูกดำเนินการตามไปด้วย เช่น การเพิ่ม การลบ หรือการอัปเดต
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")
