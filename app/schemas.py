## Schema 层（Pydantic数据模型）
# 作用：
# 数据验证：自动校验类型、格式（如EmailStr）
# 数据转换：JSON ↔ Python对象
# API文档：自动生成OpenAPI文档
# 请求体定义：POST请求的参数模板

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ========== User 相关 ==========
class UserCreate(BaseModel):  # post请求 BaseModel:数据验证、数据转换、自动生成文档
    username: str
    email: EmailStr  # 自动验证邮箱格式
    password: str
    # username: str = Field(..., min_length=3, max_length=50)
    # email: EmailStr
    # password: str = Field(..., min_length=8)  # 自动验证密码长度



class UserUpdate(BaseModel):  # put请求
    username: Optional[str] = None # 可以是 str 或 None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel): # get请求
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:   # Pydantic V2 保底，处理各种来源数据
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