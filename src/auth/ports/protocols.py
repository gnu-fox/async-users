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

    def __init__(self, session : Session):
        self.session = session

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