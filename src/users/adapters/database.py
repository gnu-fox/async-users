from typing import Union

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.users.adapters.repository import Accounts

class Database:
    def __init__(self, url : Union[str, URL]):
        self.__async_engine = create_async_engine(url=url)
        self.__async_session_factory = async_sessionmaker(
            bind = self.__async_engine,
            expire_on_commit = False,
            autoflush = False,
            class_ = AsyncSession
        )

        self.tables = {
            'accounts' : Accounts(session=None)
        }

    @property
    def session(self) -> AsyncSession:
        async_session = self.__async_session_factory()
        for table in self.tables:
            table.__init__(async_session)
        return async_session