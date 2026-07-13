## Pydantic 数据模型

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ========== User 相关 ==========
class UserCreate(BaseModel):  # post请求 BaseModel:数据验证、数据转换、自动生成文档
    username: str
    email: EmailStr  # 自动验证邮箱格式
    password: str
    # password: str = Field(..., min_length=6)  # 自动验证密码长度

class UserUpdate(BaseModel):  # put请求
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel): # get请求
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# ========== Product 相关 ==========
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    created_at: datetime

    class Config:
        from_attributes = True