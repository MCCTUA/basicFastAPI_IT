# Import Base มาก่อน
# app.models.base_class คือที่อยู่ของไฟล์ base_class.py โดย app/model/base_class.py เราเรียก app.models.base_class และ import Base มาจากไฟล์นั base_class.py
from app.models.base_class import Base

# Import Models ทั้งหมดที่อยากให้สร้างตาราง
from app.models.user import User
from app.models.item import Item

# สรุป: ไฟล์นี้มีหน้าที่รวมญาติ เพื่อให้ Alembic import ไปใช้ที่เดียวจบ
# โดยไม่ต้องไปไล่ import ทีละไฟล์ model
