from fastapi import FastAPI, HTTPException

# นำเข้า BaseModel จาก Pydantic เพื่อใช้ในการสร้างโมเดลข้อมูล
from pydantic import BaseModel

# กำหนด type list และ Optional
from typing import List, Optional


# นำเข้า get_scalar_api_reference จาก scalar_fastapi  ช่วยในการสร้างเอกสาร API
from scalar_fastapi import get_scalar_api_reference

# Create an instance of the FastAPI application
app = FastAPI()

# 1. จำลอง Database (In-Memory Database)
fake_db = [
    {"id": 1, "name": "Product 1", "price": 100, "stock": 10},
    {"id": 2, "name": "Product 2", "price": 200, "stock": 5},
]


# 2. สร้าง schema สำหรับรับ/ส่งข้อมูล
class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int


# 2.1 สำหรับ update ข้อมูลบางส่วน
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


# สร้างเส้นทางสำหรับดึงเอกสาร API reference (scalar API reference)
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        # title="My FastAPI Scalar API Reference",
        title=app.title,
    )


# สร้างเส้นทาง (route) พื้นฐาน
@app.get("/")
def read_root():
    return {"message": "CRUD Page"}


# --- API Endpoints ---


# [R]ead All: ดูสินค้าทั้งหมด
@app.get("/products", response_model=List[Product])
def get_products():
    return fake_db


# [R]ead One: ดูสินค้าตาม ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    # วนลูหา product ที่มี id ตรงกับ product_id
    for product in fake_db:
        if product["id"] == product_id:
            return product
    # ถ้าไม่พบสินค้า ให้ส่งข้อความแจ้งเตือน
    # raise คือการส่งข้อผิดพลาด HTTPException กลับไปยังผู้ใช้ ถ้าไม่มีข้อผิดพลาด จะไม่ถูกเรียกใช้
    raise HTTPException(status_code=404, detail="Product not found")


# [C]reate: สร้างสินค้าใหม่
@app.post("/products", response_model=Product, status_code=201)
# กำหนดให้ product เป็นชนิดของ Product model
def create_product(product: Product):
    # เช็คว่ามีสินค้าที่มี id เดียวกันอยู่ในฐานข้อมูลหรือไม่
    for p in fake_db:
        if p["id"] == product.id:
            raise HTTPException(
                status_code=400, detail="Product with this ID already exists"
            )
    # แปลงข้อมูล product เป็น dict ด้วย model.dump() แล้วเพิ่มเข้าไปในฐานข้อมูล
    fake_db.append(product.model_dump())
    return product


# [U]pdate: อัพเดตข้อมูลสินค้า
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, update_data: ProductUpdate):
    # enumerate() ช่วยให้เราสามารถเข้าถึง index และ value ของรายการในลูปได้
    for index, product in enumerate(fake_db):
        if product["id"] == product_id:
            # ขั้นตอนการ Copy ข้อมูลเดิม แล้วทับด้วยข้อมูลใหม่เฉพาะที่มีการส่งมา
            # 1. ** เพื่อแตก dict เป็น key-value pairs (keyword arguments)
            store_item_model = Product(**product)
            # 2. model_dump(exclude_unset=True) เพื่อดึงเฉพาะข้อมูลที่เลือกมาอัพเดตเท่านั้น
            updated_data_dict = update_data.model_dump(exclude_unset=True)
            # 3. model_copy(update=...) เพื่อสร้างสำเนาใหม่พร้อมกับอัพเดตข้อมูล
            updated_item = store_item_model.model_copy(update=updated_data_dict)

            # บันทึกข้อมูลที่อัพเดตลงในฐานข้อมูล
            fake_db[index] = updated_item.model_dump()
            return updated_item
    raise HTTPException(status_code=404, detail="Product not found")


# [D]elete: ลบสินค้า
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(fake_db):
        if product["id"] == product_id:
            fake_db.pop(index)
            return {"message": f"Product ID {product_id} deleted successfully."}
    raise HTTPException(status_code=404, detail="Product not found")


# ---------------------#
