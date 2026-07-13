---

# 🚀 从 0 到 1 开发 FastAPI 项目（开发日记）

---

## 📋 第一步：明确需求

**在写任何代码之前，先想清楚：我要做什么？**

```
需求：做一个用户管理系统
功能：
  - 创建用户（注册）
  - 查看用户列表
  - 查看单个用户
  - 更新用户信息
  - 删除用户

用户数据：
  - id（自动生成）
  - 用户名
  - 邮箱
  - 密码
  - 创建时间
```

---

## 🚀 第二步：初始化项目环境

### 2.1 创建项目目录

```bash
# 在终端执行
mkdir my_project
cd my_project
```

### 2.2 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.3 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy
```

### 2.4 创建项目结构

```bash
# 创建目录和空文件
mkdir app
mkdir app\routers

# 创建空文件（Windows）
type nul > app\__init__.py
type nul > app\routers\__init__.py
type nul > app\main.py
type nul > app\database.py
type nul > app\models.py
type nul > app\schemas.py
type nul > app\crud.py
```

> **现在目录结构：**
> ```
> my_project/
> ├── venv/
> ├── app/
> │   ├── __init__.py
> │   ├── main.py
> │   ├── database.py
> │   ├── models.py
> │   ├── schemas.py
> │   ├── crud.py
> │   └── routers/
> │       └── __init__.py
> └── requirements.txt
> ```

---

## 🚀 第三步：从 database.py 开始写

**问自己：** 我怎么连接数据库？

```python
# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 告诉 SQLAlchemy：我要用 SQLite，数据库文件叫 demo.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./demo.db"

# 2. 创建"引擎"——负责真正和数据库通信
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 3. 创建"会话工厂"——每次请求用它生成一个会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 创建"基类"——所有表模型都要继承它
Base = declarative_base()

# 5. 写一个函数：每个接口通过它获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db  # 把会话交给接口使用
    finally:
        db.close()  # 用完关闭
```

---

## 🚀 第四步：写 models.py（定义表结构）

**问自己：** 我要存什么数据？表长什么样？

```python
# app/models.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base  # 从 database.py 导入 Base

# 用户表
class User(Base):
    __tablename__ = "users"  # 表名

    # 字段定义
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

**写完后想：** 我现在定义了表结构，但数据库里还没创建。等 main.py 里执行 `create_all()` 才会真正创建。

---

## 🚀 第五步：写 schemas.py（定义数据格式）

**问自己：** 前端传什么格式？我返回什么格式？

```python
# app/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# 1. 创建用户时，前端要传什么？（必填）
class UserCreate(BaseModel):
    username: str
    email: EmailStr  # 自动验证邮箱格式
    password: str

# 2. 更新用户时，前端要传什么？（全部可选）
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# 3. 查询用户时，我返回什么？（不含密码）
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # 允许从 SQLAlchemy 对象自动转换
```

---

## 🚀 第六步：写 crud.py（数据库操作）

**问自己：** 我需要哪些数据库操作？

```python
# app/crud.py

from sqlalchemy.orm import Session
from app import models, schemas

# 1. 查询单个用户（根据 ID）
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 2. 查询单个用户（根据用户名）
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# 3. 查询所有用户（分页）
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# 4. 创建用户
def create_user(db: Session, user: schemas.UserCreate):
    # 把 Pydantic 模型转成 SQLAlchemy 模型
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    db.add(db_user)   # 添加到会话（暂存）
    db.commit()       # ⭐ 执行 INSERT SQL
    db.refresh(db_user)  # 获取数据库生成的数据（如 id）
    return db_user

# 5. 更新用户
def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # 只更新传了的字段
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()  # ⭐ 执行 UPDATE SQL
    db.refresh(db_user)
    return db_user

# 6. 删除用户
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    db.delete(db_user)  # ⭐ 执行 DELETE SQL
    db.commit()
    return db_user
```

---

## 🚀 第七步：写 routers/users.py（路由）

**问自己：** 用户模块有哪些接口？

```python
# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas, crud

# 创建路由器
router = APIRouter(prefix="/api/users", tags=["用户管理"])

# 1. GET /api/users → 获取所有用户
@router.get("/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

# 2. GET /api/users/{user_id} → 获取单个用户
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

# 3. POST /api/users → 创建用户
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return crud.create_user(db, user)

# 4. PUT /api/users/{user_id} → 更新用户
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

# 5. DELETE /api/users/{user_id} → 删除用户
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 0, "message": "删除成功"}
```

---

## 🚀 第八步：写 routers/__init__.py

```python
# app/routers/__init__.py
# 空文件，标识 routers 是一个 Python 包
```

---

## 🚀 第九步：写 main.py（入口）

**问自己：** 怎么把所有东西组装起来？

```python
# app/main.py

from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import users

# ⭐ 关键：创建数据库表（首次运行）
# 读取 models.py 中所有继承 Base 的类，执行 CREATE TABLE
models.Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title="用户管理系统 API",
    description="从零开始的 FastAPI 项目",
    version="1.0.0"
)

# 注册路由
app.include_router(users.router)

# 根路径
@app.get("/")
def root():
    return {"message": "Hello FastAPI!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)
```

---

## 🚀 第十步：写 requirements.txt

```txt
fastapi==0.139.0
uvicorn==0.51.0
sqlalchemy==2.0.23
```

---

## 🚀 第十一步：运行测试

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python -m app.main

# 3. 浏览器访问
# http://127.0.0.1:8080/docs
```

---

## ✅ 完整开发流程总结

```text
1. 明确需求
   └── 我要做什么功能？

2. 初始化环境
   └── 创建目录、虚拟环境、安装依赖

3. database.py
   └── 配置数据库连接

4. models.py
   └── 定义表结构

5. schemas.py
   └── 定义输入/输出数据格式

6. crud.py
   └── 写数据库操作函数

7. routers/xxx.py
   └── 写接口路由

8. main.py
   └── 组装所有模块，启动服务

9. 测试
   └── Swagger 测试接口
```

---

## 💡 开发时的思考顺序

| 步骤 | 问自己 |
|:---|:---|
| 第 1 步 | 我要做什么？ |
| 第 2 步 | 我怎么连数据库？ |
| 第 3 步 | 我要存什么数据？ |
| 第 4 步 | 前端传什么？我返回什么？ |
| 第 5 步 | 我需要哪些数据库操作？ |
| 第 6 步 | 有哪些接口？URL 是什么？ |
| 第 7 步 | 怎么组装和启动？ |

---

**这就是从 0 到 1 的完整开发过程！每一步都清晰可循，照着这个顺序写，永远不会乱。** 🚀😊