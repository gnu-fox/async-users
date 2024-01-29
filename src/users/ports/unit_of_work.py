from abc import ABC, abstractmethod
from typing import Protocol, Callable

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


class UnitOfWork(ABC):
    def __init__(self, session : Session): 
        self.__session = session
    
    @abstractmethod
    async def begin(self):
        ...

    async def __aenter__(self):
        self.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()
        
    async def commit(self):
        await self.__session.commit()

    async def rollback(self):
        await self.__session.rollback()

    async def close(self):
        await self.__session.commit()
        await self.__session.close()


class Repositories(UnitOfWork):
    accounts : Accounts
    credentials : Credentials 

    def __init__(self, session: Session):
        super().__init__(session)