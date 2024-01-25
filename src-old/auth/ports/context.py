from abc import ABC, abstractmethod
from typing import Protocol, List

from src.messagebus import Context
from src.auth.ports.repository import Accounts

class Session(Protocol):
    def commit(self):
        ...

    def rollback(self):
        ...

    def close(self):
        ...

class ORM(Protocol):

    @property
    def session(self) -> Session:
        ...
        
class UOW(ABC):

    def __init__(self, session : Session):
        self.session = session
    
    @abstractmethod
    def begin(self):
        pass

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()

    def __enter__(self):
        self.begin()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.close()
        

class Users(UOW):

    def __init__(self, orm : ORM):
        self.orm = orm

    def begin(self):
        self.session = self.orm.session
        
