from typing import Any
from typing import Union

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.settings import Settings
from src.users.models import Account
from src.users.models import Credentials
from src.backend.gateway import Accounts

class SessionFactory:
    def __init__(self, url : Union[str, URL]):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession)

    def __call__(self) -> AsyncSession:
        return self.session_factory()

class UnitOfWork:
    def __init__(self, session_factory : SessionFactory):
        self.session_factory = session_factory

    async def __aenter__(self):
        await self.begin()
        return self
    
    async def __aexit__(self, exc_type : Any, exc_value : Any, traceback : Any):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
    
    async def begin(self):
        self.session = self.session_factory()
        self.accounts = Accounts(session = self.session)
        await self.session.begin()

    async def create(self, credentials : Credentials) -> Account:
        account = await self.accounts.create(credentials)
        return account
    
    async def read(self, credentials : Credentials) -> Account:
        account = await self.accounts.read(credentials)
        return account
    
    async def update(self, account : Account, credentials : Credentials = None):
        if credentials:
            await self.accounts.update(account, credentials)
    
    async def delete(self, account : Account):
        await self.accounts.delete(account)