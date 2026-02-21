from pydantic import BaseModel, Field, ConfigDict, EmailStr

class Users(BaseModel):
    username: str = Field(
        ...,
        examples=["nameAa"],
        description="ชื่อผู้ใช้งาน"
    )
    first_name: str = Field(
        ...,
        max_length=300,
        examples="สมชาย"
    )
    last_name: str = Field(
        ...,
        max_length=300,
        examples="นามสกุล"
    )
    email: EmailStr = Field(
        ...,
        examples="name@email.com"
    )
    is_active: bool = True

class UserCreate(Users):
    # เพิ่มฟิลด์นี้เพื่อให้ Pydantic รับค่าจาก JSON ได้
    password: str = Field(
        ..., 
        min_length=6, 
        description="รหัสผ่านสำหรับลงทะเบียน"
        )

class UserUpdate(BaseModel):
    first_name: str | None = Field(None, max_length=300)
    last_name: str | None = Field(None, max_length=300)
    email: EmailStr | None = None
    is_active: bool | None = None

class UserResponse(Users):
    id: int

    model_config = ConfigDict(from_attributes=True)

