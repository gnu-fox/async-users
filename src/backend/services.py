from typing import Any
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.settings import Settings
from src.backend.gateway import Accounts

class SessionFactory:
    def __init__(self, url : URL):
        self.engine = create_async_engine(url, future=True)
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession)

    def __call__(self) -> AsyncSession:
        return self.session_factory()


class UnitOfWork:
    def __init__(self, session_factory : SessionFactory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.accounts = Accounts(session = self.session)
        await self.session.begin()
        return self
    
    async def __aexit__(self, exc_type : Any, exc_value : Any, traceback : Any):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()