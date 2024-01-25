from uuid import uuid4
from typing import Union, Generator, Any

from passlib.context import CryptContext
from sqlalchemy import URL
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.auth.adapters.async_sqlalchemy.schemas import Account as Schema
from src.auth.domain.aggregates import Account, ID

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Accounts:

    def __init__(self, session : AsyncSession):
        self.session = session

    async def create(self, username : str, password : str):
        hash = context.hash(password)
        async with self.session as session:
            try:
                statement = insert(Schema).values(id=uuid4(), username=username, password=hash)
                await session.execute(statement)
                await session.commit()

            except Exception as exception:
                await session.rollback()
                raise exception


    async def read(self, **kwargs) -> Union[Account, None]:
        async with self.session as session:
            try:
                statement = select(Schema).filter_by(**kwargs)
                result = await session.execute(statement)
                schema = result.scalars().first()
            
            except Exception as exception:
                await session.rollback()
                raise exception
            

    async def delete(self, id : ID):
        async with self.session as session:
            try:
                statement = delete(Schema).where(Schema.id == id)
                await session.execute(statement)
                await session.commit()
            
            except Exception as exception:
                await session.rollback()
                raise exception
