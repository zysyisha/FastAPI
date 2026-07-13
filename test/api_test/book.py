# # 类似于django里的 path
# from fastapi import APIRouter
# #生成路由对象
# api_book = APIRouter()
#
# @api_book.get("/get")
# async def get_test():
#     return {"method":"get方法"}
#
# @api_book.post("/post")
# async def post_test():
#     return {"method":"post方法"}
#
# @api_book.put("/put")
# async def put_test():
#     return {"method": "put方法"}
#
# @api_book.delete("/delete")
# async def delete_test():
#     return {"method":"delete方法"}