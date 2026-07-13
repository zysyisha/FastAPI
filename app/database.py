## 数据库配置

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 数据库连接
SQLALCHEMY_DATABASE_URL = "sqlite:///./demo.db"

# 创建引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 专用
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 负责收集表结构定义，create_all() 负责把收集到的定义真正创建到数据库里。

# 创建 Base 类（用于定义模型）Base 是 SQLAlchemy 的“模型工厂”，它让你能用 Python 类来定义数据库表结构，省去了手写 SQL 建表语句的麻烦。这也是 ORM（对象关系映射） 最核心的体现：你把数据库表映射成了一个 Python 类来操作。
Base = declarative_base()


# 依赖注入：获取数据库会话
def get_db():
    db = SessionLocal()  # 创建一个数据库会话（连接）
    try:
        yield db   # 把这个会话交给接口函数使用
    finally:
        db.close()   # 接口函数执行完毕后，关闭会话