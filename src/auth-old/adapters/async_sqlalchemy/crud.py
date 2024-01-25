from uuid import uuid4
from typing import Union, Generator, Any

from sqlalchemy import URL
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from passlib.context import CryptContext

from src.auth.adapters.async_sqlalchemy.schemas import Account as Schema
from src.auth.domain.aggregates import Account
from src.auth.domain.models import SecretStr, ID


context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ORM:
    def __init__(self, url : str):
        self.__engine = create_async_engine(url)
        self.__async_session_factory = async_sessionmaker(self.__engine, expire_on_commit=False, class_=AsyncSession)
        self.__session : AsyncSession = None

    async def __aenter__(self):
        self.__session = self.__async_session_factory()
        return self.__session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__session.close()


class Accounts:
    def __init__(self, session : AsyncSession):
        self.__session = session

    async def create(self, username : str, password : SecretStr):
        hash = context.hash(password.get_secret_value())
        async with self.__session as session:
            try:
                statement = insert(Schema).values(id=uuid4(), username=username, password=hash)
                await session.execute(statement)
                await session.commit()

            except Exception as exception:
                await session.rollback()
                raise exception


    async def read(self, **kwargs) -> Union[Account, None]:
        async with self.__session as session:
            try:
                statement = select(Schema).filter_by(**kwargs)
                result = await session.execute(statement)
                schema = result.scalars().first()
                if schema:
                    account = Account(id=schema.id, username=schema.username)
                    return account
                
                return None
            
            except Exception as exception:
                await session.rollback()
                raise exception
            
                
    async def delete(self, id: ID):
        async with self.__session as session:
            try:
                statement = delete(Schema).where(Schema.id == id)
                await session.execute(statement)
                await session.commit()

            except Exception as exception:
                await session.rollback()
                raise exception