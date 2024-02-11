from typing import Any
from typing import Union

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.domain.models import Account
from src.domain.models import User
from src.domain.models import Credentials
from src.adapters.data_access_objects import Accounts

class SessionFactory:
    def __init__(self, url : Union[str, URL]):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession)

    def __call__(self) -> AsyncSession:
        return self.session_factory()
    

class UnitOfWork:
    def __init__(self, session_factory : SessionFactory):
        self.session_factory = session_factory

    async def begin(self):
        self.session = self.session_factory()
        self.accounts = Accounts(session=self.session)
        await self.session.begin()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        await self.begin()
        return self
    
    async def __aexit__(self, exc_type : Any, exc_value : Any, traceback : Any):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()


class Users(UnitOfWork):
    def __init__(self, session_factory: SessionFactory):
        super().__init__(session_factory)

    async def create(self, credentials : Credentials):
        await self.accounts.create(credentials)
    
    async def read(self, credentials : Credentials) -> User:
        account = await self.accounts.read(credentials)
        user = User(account)
        return user
    
    async def update(self, user : User, credentials : Credentials = None):
        if credentials:
            await self.accounts.update(user.account, credentials)
    
    async def delete(self, user : User):
        await self.accounts.delete(user.account)