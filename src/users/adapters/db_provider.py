from typing import Union

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.users.adapters.accounts import Accounts
from src.users.adapters.credentials import Credentials

class ORM:

    def __init__(self, url : Union[str, URL], expire_on_commit : bool = True, autoflush : bool = True):
        self.__async_engine = create_async_engine(url=url)
        self.__async_session_factory = async_sessionmaker(
            bind = self.__async_engine,
            expire_on_commit = expire_on_commit,
            autoflush = autoflush,
            class_ = AsyncSession
        )

    async def dispose(self):
        await self.__async_engine.dispose()

    @property
    def session_factory(self):
        return self.__async_session_factory


class Provider:

    def __init__(self, orm : ORM):
        self.__orm = orm

    @property
    def session_factory(self):
        return self.__orm.session_factory

    @property
    def accounts(self) -> Accounts:
        return Accounts(session = None)
    
    @property
    def credentials(self) -> Credentials:
        return Credentials(session = None)