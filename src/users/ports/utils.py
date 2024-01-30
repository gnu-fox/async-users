from abc import ABC, abstractmethod
from typing import Protocol, Callable

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
    
    async def commit(self):
        await self.__session.commit()

    async def rollback(self):
        await self.__session.rollback()

    async def close(self):
        await self.__session.commit()
        await self.__session.close()

    async def __aenter__(self):
        self.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.rollback()
        self.close()


class DataAccessObject(ABC):
    def __init__(self, session : Session):
        self.session = session


class Repository(UnitOfWork):
    def __init__(self, sessionmaker : Callable[[],Session]):
        self.__session_factory = sessionmaker

    async def begin(self):
        session = self.__session_factory()
        super().__init__(session)
        for _, attribute_value in self.__dict__.items():
            if isinstance(attribute_value, DataAccessObject):
                attribute_value.__init__(session)
        await session.begin()



class Repository(UnitOfWork):
    session_factory : Callable[[],Session]

    def __init__(self):
        self.__session_factory = self.session_factory

    async def begin(self):
        if not self.__session_factory:
            raise Exception("Set a session factory for the repository class")
        
        session = self.__session_factory()
        super().__init__(session)
        for _, attribute_value in self.__dict__.items():
            if isinstance(attribute_value, DataAccessObject):
                attribute_value.__init__(session)
        await session.begin()