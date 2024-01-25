from abc import ABC, abstractmethod
from typing import Protocol, Generic, TypeVar

class Session(Protocol):
    async def begin(self):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def close(self):
        ...
        

T, ID = TypeVar('T'), TypeVar('ID')
class CRUD(ABC, Generic[T]):

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def read(self, **kwargs) -> T:
        pass

    @abstractmethod
    async def delete(self, id : ID):
        pass


class ORM(Protocol):

    @property
    def session(self) -> Session:
        ...

    @property
    def repositories(self) -> dict[str, CRUD]:
        ...

class UOW:
    def __init__(self, orm : ORM):
        self.__orm = orm

    async def __aenter__(self):
        self.__session = self.__orm.session
        await self.__session.begin()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__session.rollback()
        await self.__session.close()

    async def commit(self):
        await self.__session.commit()
    