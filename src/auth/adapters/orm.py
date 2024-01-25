from typing import Union, Dict

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.auth.adapters.crud import Accounts

class ORM:
    def __init__(self, url : Union[str, URL]):
        self.url = url
        self.engine = create_async_engine(url=self.url)
        self.async_session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False)
        self.repositories = {
            'accounts': Accounts(session=None)
        }

    @property
    def session(self) -> AsyncSession:
        session = self.async_session_factory()
        for repository in self.repositories.values():
            repository.session = session
        return session