from typing import Protocol

class Accounts:
    pass

class Credentials:
    pass

class AsyncSession(Protocol):

    async def begin(self):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def close(self):
        ...


class AsyncUnitOfWork:
    def __init__(self, session : AsyncSession):
        self.__session = session

    async def __aenter__(self):
        await self.__session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__session.rollback()
        await self.__session.close()

    async def begin(self):
        await self.__session.begin()

    async def commit(self):
        await self.__session.commit()



from typing import Union
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

class Context(AsyncUnitOfWork):
    def __init__(self, url : Union[str, URL], autoflush : bool = True):
        self.__async_engine = create_async_engine(url=url)
        self.__async_session_factory = async_sessionmaker(
            bind = self.__async_engine,
            expire_on_commit = False,
            autoflush = autoflush,
            class_ = AsyncSession
        )
        self.__async_session = self.__async_session_factory()
        super().__init__(self.__session)

        self.accounts = Accounts(session=self.__async_session),
        self.credentials = Credentials(session=self.__async_session)