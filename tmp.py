import os
import dotenv
from uuid import uuid4
from typing import Union

from sqlalchemy import URL
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.auth.adapters.async_sqlalchemy.schemas import Account as Schema
from src.auth.domain.aggregates import Account
from src.auth.domain.models import SecretStr, ID


dotenv.load_dotenv()
url = URL.create(
    drivername = 'postgresql+asyncpg',
    username = os.getenv('TEST_DATABASE_USERNAME'),
    password = os.getenv('TEST_DATABASE_PASSWORD'),
    host = os.getenv('TEST_DATABASE_HOST'),
    port = os.getenv('TEST_DATABASE_PORT'),
    database = os.getenv('TEST_DATABASE_NAME'))

class Accounts:

    def __init__(self, session : AsyncSession):
        self.session = session

    async def create(self, username : str, password : str):
        statement = insert(Schema).values(id=uuid4(), username=username, password=password)
        await self.session.execute(statement)                

    async def read(self, **kwargs) -> Union[Account, None]:
        statement = select(Schema).filter_by(**kwargs)
        result = await self.session.execute(statement)
        schema = result.scalars().first()

        if schema:
            account = Account(id=schema.id, username=schema.username)
            return account
        
        return None
    
    async def delete(self, id : ID):
        statement = delete(Schema).filter_by(id=id)
        await self.session.execute(statement)

class ORM:
    def __init__(self, url : Union[str, URL]):
        self.url = url
        self.engine = create_async_engine(url=self.url)
        self.async_session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    @property
    def session(self) -> AsyncSession:
        return self.async_session_factory()
    
orm = ORM(url)

class Users:
    database_url : Union[str, URL] = None

    def __init__(self):
        self.accounts = Accounts(session = None)

    async def __aenter__(self):
        session = orm.session
        self.accounts.session = session
        await session.begin()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.accounts.session.rollback()
        await self.accounts.session.close()

    async def commit(self):
        await self.accounts.session.commit()

        
async def main():
    users = Users()

    async with users:
        await users.accounts.create(username='test', password='test')
        account = await users.accounts.read(username='test')
        assert account.username == 'test'
        print(account.id)
        await users.accounts.delete(id=account.id)
        account = await users.accounts.read(username='test')
        assert account is None
        await users.commit()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

