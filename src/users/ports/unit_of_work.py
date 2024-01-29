from typing import Protocol

from src.users.ports.accounts import Accounts
from src.users.ports.credentials import Credentials

class Session(Protocol):

    async def begin(self):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def close(self):
        ...


class UnitOfWork:
    def __init__(self, session : Session):
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


class Repositories(UnitOfWork):
    accounts : Accounts
    credentials : Credentials 

    def __init__(self, session: Session):
        super().__init__(session)