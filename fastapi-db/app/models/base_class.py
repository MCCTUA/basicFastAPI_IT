from sqlalchemy.orm import DeclarativeBase


# สร้าง Base Class ก่อน เพื่อให้ทุก Model สืบทอดมาจากตัวนี้
# DeclarativeBase มาจาก SQLAlchemy ORM
# Base Class นี้จะใช้สำหรับสร้าง Model ต่าง ๆ ในฐานข้อมูล
# การสร้าง Base Class ช่วยให้เราจัดการกับ Model ได้ง่ายขึ้น
# เช่น การสร้างตารางในฐานข้อมูล หรือการทำงานร่วมกับ session
# Base Class นี้จะไม่มีตารางในฐานข้อมูลเอง แต่จะเป็นแม่แบบให้ Model อื่น ๆ สืบทอด
# การใช้ DeclarativeBase ช่วยให้เราสามารถใช้ฟีเจอร์ต่าง ๆ ของ SQLAlchemy ORM ได้อย่างเต็มที่
# เช่น การแมปคลาสกับตารางในฐานข้อมูล การกำหนดความสัมพันธ์ระหว่างตาราง ฯลฯ
# นอกจากนี้ยังช่วยให้โค้ดมีความเป็นระเบียบและง่ายต่อการดูแลรักษา
# pass คือ การบอกว่าไม่มีการเพิ่มฟีเจอร์พิเศษใด ๆ ใน Base Class นี้
class Base(DeclarativeBase):
    pass


# ตอนนี้เรามี Base Class ที่ใช้สำหรับสร้าง Model ต่าง ๆ ในฐานข้อมูลแล้ว
# Model ต่าง ๆ จะสืบทอดมาจาก Base Class นี้ เช่น: Class User สือบทมาจาก Base
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
# ซึ่งจะช่วยให้เราจัดการกับฐานข้อมูลได้ง่ายขึ้นผ่าน SQLAlchemy ORM
