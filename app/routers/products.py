## 商品路由

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/api/products", tags=["商品管理"])

@router.get("/", response_model=List[schemas.ProductResponse])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return db_product

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return {"code": 0, "message": "删除成功"}