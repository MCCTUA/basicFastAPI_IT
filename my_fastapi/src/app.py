from fastapi import FastAPI

# นำเข้า BaseModel จาก Pydantic เพื่อใช้ในการสร้างโมเดลข้อมูล
from pydantic import BaseModel

# นำเข้า get_scalar_api_reference จาก scalar_fastapi  ช่วยในการสร้างเอกสาร API
from scalar_fastapi import get_scalar_api_reference

# Create an instance of the FastAPI application
app = FastAPI()


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
    return {"message": "Hello, World!"}


@app.get("/about")
def read_about():
    return {"message": "This is the about page."}


# ---- CRUD Operations ----#


@app.get("/products")
def read_products():
    return {"products": ["Product 1", "Product 2", "Product 3"]}


@app.post("/products")
def create_product(name: str):
    return {"message": f"Product '{name}' created successfully."}


@app.put("/products/{product_id}")
def update_product(product_id: int, name: str):
    return {"message": f"Product ID {product_id} updated to '{name}'."}


@app.patch("/products/{product_id}")
def partial_update_product(product_id: int, name: str = None):
    return {"message": f"Product ID {product_id} partially updated to '{name}'."}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {"message": f"Product ID {product_id} deleted successfully."}


# ---------------------#


# route แบบมี parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "item_id+1 =": item_id + 1, "q": q}


# route แบบมี query parameter
@app.get("/items/")
def search_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# route แบบมีการส่งข้อมูลใน body ของคำขอ (JSON body)
#  ใช้ Pydantic model เพื่อกำหนดโครงสร้างข้อมูล (schema) ซึ่งเป็นพิมพ์เขียวสำหรับข้อมูลที่คาดว่าจะได้รับ จาก request body
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


# route สำหรับสร้าง item ใหม่จากข้อมูลใน request body
@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "price_with_tax": item.price * 1.07}
