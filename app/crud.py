## 数据库操作  用python写sql
# Service/CRUD 层
# 作用：
# 业务逻辑：协调Schema和Model
# 数据库操作：增删改查的具体实现
# 事务管理：commit/rollback控制

# 注意：只有继承BaseModel才是pydantic模型，主要为了验证数据来的，而orm就是关联数据库，说白了就是python写sql！两者区分开

from sqlalchemy.orm import Session
from app import models, schemas


# ========== User CRUD ==========
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# 相当于写sql语句
def create_user(db: Session, user: schemas.UserCreate):
    # 检查唯一性
    # existing = db.query(models.User).filter(
    #     (models.User.username == user.username) |
    #     (models.User.email == user.email)
    # ).first()
    # if existing:
    #     raise HTTPException(400, "用户已存在")
    #
    # # 密码加密
    # hashed = pwd_context.hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password  # 生产环境要用 bcrypt 加密！
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


# ========== Product CRUD ==========
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None

    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return None

    db.delete(db_product)
    db.commit()
    return db_product