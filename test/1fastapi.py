# # web框架
# from fastapi import FastAPI
#
# # web服务器
# import uvicorn
# from pydantic import BaseModel
#
# from test.api.book import api_book
# from test.api.cbs import api_cbs
# from test.api.zz import api_zz
#
# app = FastAPI()
# # 类似于django 的 include
# app.include_router(api_book, prefix="/book", tags=["图书接口", ])
# app.include_router(api_cbs, prefix="/cbs", tags=["出版接口", ])
# app.include_router(api_zz, prefix="/zz", tags=["作者口", ])
#
# @app.get("/")
# async def root():
#     return {"message": "Hello B站程序员"}
#
# @app.get("/get")
# def get_test():
#     return {"method":"get方法"}
#
# @app.post("/post")
# def post_test():
#     return {"method":"post方法"}
#
# @app.put("/put")
# def put_test():
#     return {"method":"put方法"}
#
# @app.delete("/delete")
# def delete_test():
#     return {"method": "delete方法"}
#
# # 加入Request
#
# # @app.get("/get_test")
# # async def get_test(request:Request):
# #     get_test = request.path_params
# #     print(get_test)
# #     return {"method":"test_test"}
#
# # @app.post("/post_test")
# # async def post_test(request: Request):
# #     post_test = await request.json()
# #     print(post_test)
# #     return {"method":"post_test"}
#
# # 定义数据模型
# class User(BaseModel):
#     name: str
#     age: int
#
# @app.get("/get_test")
# async def get_test(name: str, age: int):
#     return {"name": name, "age": age}
#
# @app.post("/post_test")
# async def post_test(user: User):  # ← 注意：这里定义的是 user: User，不是 request: Request
#     print(f"收到: {user.name}, {user.age}")
#     return {"received": {"name": user.name, "age": user.age}}
#
# if __name__ == '__main__':
#     uvicorn.run("1fastapi:app", host="127.0.0.1", port=8080, reload=True)