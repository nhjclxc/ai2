# https://sqlalchemy.flask.org.cn/en/3.1.x/queries/


from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Query, Depends, HTTPException, Body
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, update, select, Sequence
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import Annotated, List, Dict, Optional

from sqlalchemy.sql.functions import user

from sql02_database_async_connect import MYSQL_ASYNC_ENGINE, MYSQL_ASYNC_AsyncSessionLocal

engine:AsyncEngine = MYSQL_ASYNC_ENGINE
AsyncSessionLocal = MYSQL_ASYNC_AsyncSessionLocal

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    addr = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    desc = Column(String(50), nullable=False)

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "addr": self.addr,
            "email": self.email,
            "desc": self.desc,
        }

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("init db success")

@asynccontextmanager
async def get_session(SessionLocal):
    """
    get_session
        支持自动管理事务
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# create
## create orm
async def create_user(user:User):
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        # session.add使用的是 orm，不需要使用sql
        session.add(user)
        await session.refresh(user)
        print(f"create user result id {user.id}")
        return user

## create Core[sql]
async def create_user_insert(user:User) -> User:
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        # .returning(User.id) 表示要把id数据返回
        stmt = insert(User).values(name=user.name, age=user.age, addr=user.addr, desc=user.desc).returning(User.id)
        # session.execute insert(User) 实际使用的是 insert into ... 的sql语句
        result = await session.execute(stmt)
        await session.commit()
        user.id = result.scalar()  # 拿到自增 id
        return user

## create batch orm
async def batch_create_user(users: List[User]) -> int:
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        session.add_all(users)
        await session.commit()
        print(f"batch_create_user create user result id {len(users)}")
        return len(users)

## create batch Core[sql]， 大批量高性能推荐使用这种，原生sql方式
async def batch_create_user_insert(users:List[User]) -> int:
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        # 实现 insert into 的批量插入
        # 第一个是：statement， 第二个是：params
        await session.execute(insert(User), [u.to_dict() for u in users])
        await session.commit()
        return len(users)


# update
## update orm
async def update_user(user: User) -> bool:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        # 第一个是 ORM 到实体对象，第二个是这个实体（表）的主键
        user_db = await session.get(User, user.id)
        if not user_db:
            raise HTTPException(404, "User not found")
        user_db.addr = user.addr
        user_db.desc = user.desc
        # 使用了 get_session 之后自动提交事务，无须在使用 session.commit()
        return True

## update core
async def update_user_core(user: User) -> bool:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        # stmt -> statement -> sql语句
        # stmt update(User).where(User.id == user.id).values(user.to_dict())
        stmt = update(User).where(User.id == user.id).values(addr=user.addr, desc=user.desc)
        result =  await session.execute(stmt)
        return int(result.rowcount) == 1

## update orm batch
async def batch_update_user(users: List[User]) -> int:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        # update
        user_ids = [u.id for u in users]
        user_dict: Dict[int, User] = {user.id: user for user in users}
        # 1 查询所有对应的数据
        # 在 SQLAlchemy 中，查询某个字段是否在列表里，要用 in_() 方法。
        result = await session.execute(select(User).where(User.id.in_(user_ids)))
        users_db = result.scalars().all()
        # 2 修改相关对象的数据
        for user in users_db:
            ext_user = user_dict[user.id]
            user.addr = ext_user.addr
            user.desc = ext_user.desc
        # 3 自动提交事务

        return len(users_db)

## update core batch
async def batch_update_user_core(users: List[User]) -> int:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession

        total = 0
        for user in users:
            # 为每一个 user 构造一条sql
            stmt = (
                update(User)
                .where(User.id == user.id)
                .values(addr=user.addr, desc=user.desc)
            )
            result = await session.execute(stmt)
            total += result.rowcount or 0  # rowcount 可能为 None

        await session.commit()
        return total


# select
# select orm
async def select_user_by_id(user_id: int) -> User:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        # user: User | None  # Python 3.10+ 支持的写法
        # 最新等价写法：user: Optional[User]
        # 意思是：user 可能是一个 User 实例 或者 user 可能为 None
        user: Optional[User] = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return user

# select core
async def select_user_by_cond(user_cond: User) -> Sequence[User]:
    async with get_session(AsyncSessionLocal) as session:  # type: AsyncSession
        if not user_cond:
            raise HTTPException(status_code=404, detail=f"User {user_cond} not found")

        stmt = select(User)
        if user_cond.id:
            stmt = stmt.where(User.id == user_cond.id)
        if user_cond.name:
            stmt = stmt.where(User.name == user_cond.name)
        if user_cond.age is not None and user_cond.age > 0:
            stmt = stmt.where(User.age == user_cond.age)
        if user_cond.addr:
            stmt = stmt.where(User.addr == user_cond.addr)

        result = await session.execute(stmt)
        users: Sequence[User] = result.scalars().all()
        return users




# 基于fastapi的 Lifespan 上下文管理器来执行 sqlalchemy 的异步事件

# Lifespan 上下文管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动逻辑
    # 启动fastapi（web）的时候同时启动数据库（orm）
    await init_db()
    yield
    # 关闭逻辑（可选）
    await engine.dispose()
    print("✅ engine disposed")

app = FastAPI(lifespan=lifespan)

class RequestUser(BaseModel):
    # 如果允许字段为空，那么必须使用以下方法 | None = Field(default=None)
    id: int | None = Field(default=None)
    name: str | None = Field(default=None)
    age: int | None = Field(default=None)
    addr: str | None = Field(default=None)
    email: str | None = Field(default=None)
    description: str | None = Field(default=None)

    def to_orm(self) -> User:
        # entity 与 model 的字段一摸一样时使用以下方法即可
        # return User(**self.model_dump())
        # 当 entity 与 model 的字段有差异时，使用以下方法
        user_dict = self.model_dump()
        user_dict['desc'] = user_dict.pop('description')
        return User(**user_dict)

def request_user_list_to_orm_list(users: List[RequestUser]) -> List[User]:
    return [u.to_orm() for u in users if u is not None]


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)
user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@user_router.post("/c1")
async def create(req_user: RequestUser):
    print(f"req_user: {req_user}")
    user = req_user.to_orm()
    print(f"create user {user}")
    if user is None:
        raise HTTPException(400, "create user error [user obj is None]")
    if user.name is None or user.name == "":
        raise HTTPException(400, "create user error [user name is None]")
    print(f"user: {user.__dict__}")

    await create_user(user)
    return {
        "code": 200,
        "msg": "ok",
        "data": {
            "id": user.id,
        }
    }

@user_router.post("/c2")
async def batch_create(req_user_list: Annotated[List[RequestUser], Body()]):
    print(f"req_user_list len: {len(req_user_list)}")
    if len(req_user_list) == 0:
        raise HTTPException(400, "create user error [users is empty]")

    orm_list = request_user_list_to_orm_list(req_user_list)
    insert_list: List[User] = []
    for user in orm_list:
        if user is None or user.age < 18:
            continue
        insert_list.append(user)

    # insert_list = [ u for u in orm_list if u.age >= 18 ]
    print(f"create user {len(insert_list)} success")

    if len(insert_list) == 0:
        raise HTTPException(400, "create user error [users age >= 18 is empty]")

    # insert_size = 1
    # async 的函数一定要使用 await ，否则就会出现：ypeError: 'coroutine' object is not iterable
    insert_size = await batch_create_user(orm_list)
    return {
        "code": 200,
        "msg": "ok",
        "data": {
            "insert size": insert_size
        }
    }

@user_router.post("/u1")
async def update_u1(req_user: Annotated[RequestUser, Body()]):

    print(f"req_user: {req_user}")
    user = req_user.to_orm()
    print(f"create user {user}")
    await update_user(user)

    return {
        "code": 200,
        "msg": "ok",
    }


@user_router.post("/u2")
async def update_u2(req_user: Annotated[RequestUser, Body()]):

    print(f"req_user: {req_user}")
    user = req_user.to_orm()
    print(f"create user {user}")
    await update_user_core(user)

    return {
        "code": 200,
        "msg": "ok",
    }
@user_router.post("/ub1")
async def update_ub1(req_user_list: Annotated[List[RequestUser], Body()]):

    print(f"len(req_user_list): {len(req_user_list)}")
    orm_list = request_user_list_to_orm_list(req_user_list)
    print(f"len(orm_list): {len(orm_list)}")
    res = await batch_update_user(orm_list)

    return {
        "code": 200,
        "msg": "ok",
        "data": {
            "res": res,
        }
    }

@user_router.post("/ub2")
async def update_ub2(req_user_list: Annotated[List[RequestUser], Body()]):

    print(f"len(req_user_list): {len(req_user_list)}")
    orm_list = request_user_list_to_orm_list(req_user_list)
    print(f"len(orm_list): {len(orm_list)}")
    res = await batch_update_user_core(orm_list)

    return {
        "code": 200,
        "msg": "ok",
        "data": {
            "res": res,
        }
    }

@user_router.post("/r1")
async def select_r1(req_user: Annotated[RequestUser, Body()]):

    print(f"len(req_user): {req_user}")
    orm_user = req_user.to_orm()
    res = await select_user_by_id(orm_user.id)

    return {
        "code": 200,
        "msg": "ok",
        "data": {
            "res": res,
        }
    }

@user_router.post("/r2")
async def select_r2(req_user: Annotated[RequestUser, Body()]):

    print(f"len(req_user): {req_user}")
    orm_user = req_user.to_orm()
    res = await select_user_by_cond(orm_user)

    return {
        "code": 200,
        "msg": "ok",
        "data": {
            "res": res,
        }
    }



admin_router.include_router(user_router)
app.include_router(admin_router)

# fastapi dev sqlalchemy01/sql06_crud.py
