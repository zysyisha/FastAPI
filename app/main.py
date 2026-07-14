## 入口文件

from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import users, products

# 创建数据库表（首次运行自动生成）
models.Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    # title="我的项目 API",
    # description="FastAPI + SQLite 企业级结构 Demo",
    # version="1.0.0"
)

# 注册路由
app.include_router(users.router)
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Hello FastAPI + SQLite 企业级结构"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)

