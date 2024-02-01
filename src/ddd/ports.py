import logging

import functools
from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar, Generator
from typing import Set

from src.ddd.protocols import Session
from src.ddd.domain import Event, Aggregate

class DataAccessObject(ABC):

    @abstractmethod
    def __init__(self, session : Session):
        ...


class UnitOfWork(ABC):
    
    def __init__(self, session : Session):
        self.session = session

    @abstractmethod
    async def begin(self):
        ...

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.commit()
        await self.session.close()

    async def __aenter__(self):
        await self.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.close()


class Context(UnitOfWork):
    def __init__(self, session_factory : Callable[[], Session]):
        self.__session_factory = session_factory

    async def begin(self):
        self.session = self.__session_factory()
        if not self.session:
            raise Exception("Session not created")
        
        super().__init__(self.session)
        for attribute_name, attribute_value in self.__dict__.items():
            if isinstance(attribute_value, DataAccessObject):
                print(f"injecting session in {attribute_name} of class {self}")
                attribute_value.__init__(self.session)
                
        await self.session.begin()