## 用户路由

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/api/users", tags=["用户管理"])

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):  #  # ← 依赖注入 管理好这个会话的生命周期
    return crud.get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):  # 这里的 db 就是上面 yield 出来的会话，FastAPI 看到 db
    # 检查用户名是否已存在
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return crud.create_user(db, user)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 0, "message": "删除成功"}