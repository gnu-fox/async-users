from typing import Union

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.users.adapters.accounts import Accounts
from src.users.adapters.credentials import Credentials

from users.ports.unit_of_work import Repositories as UnitOfWork

class Repositories(UnitOfWork):
    def __init__(self, url : Union[str, URL], autoflush : bool = True):
        self.__async_engine = create_async_engine(url=url)
        self.__async_session_factory = async_sessionmaker(
            bind = self.__async_engine,
            expire_on_commit = False,
            autoflush = autoflush,
            class_ = AsyncSession
        )
        self.__async_session = self.__async_session_factory()
        super().__init__(self.__async_session)

        self.accounts = Accounts(session=self.__async_session)
        self.credentials = Credentials(session=self.__async_session)