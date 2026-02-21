from pydantic import Field, BaseModel, ConfigDict

class Product(BaseModel):
    name: str = Field(
        ...,
        max_length=300,
        examples=["RH-7A26-20065"],
        description="ชื่อสินค้า"
    )
    description: str | None = Field(
        None, 
        description="หมายเหตุเพิ่มเติม (ถ้ามี)",
        max_length=1000
    )
    price: float = Field(
        0,
        ge=0,
        examples=[150.50],
        description="ราคาสินค้าต่อหน่วย (ต้องมากกว่า 0)",
    )
    stock: float= Field(
        0,
        ge=0,
        examples=[100.50],
        description="จำนวนสินค้า (ต้องมากกว่า 0)",
    )
    is_active: bool = True

class ProductCreate(Product):
    pass

class ProductUpdate(BaseModel):
    name: str | None = Field(None, max_length=300)
    description: str | None = Field(None, max_length=1000)
    price: float | None = Field(None, ge=0)
    stock: float | None = Field(None, ge=0)
    is_active: bool | None = None

class ProductResponse(Product):
    id: int
    model_config = ConfigDict(from_attributes=True)
