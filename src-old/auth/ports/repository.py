from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union, Protocol

from src.messagebus import Repository
from src.auth.domain.models import SecretStr, ID
from src.auth.domain.aggregates import Account

class Session(Protocol):
    def commit(self):
        ...

    def rollback(self):
        ...

    def close(self):
        ...

T, ID = TypeVar('T'),  TypeVar('ID')
class CRUD(ABC, Generic[T]):

    @abstractmethod
    def create(self, **kwargs) -> Union[T, None]:
        pass

    @abstractmethod
    def read(self, **kwargs) -> Union[T, None]:
        pass
    
    @abstractmethod
    def delete(self, id : ID):
        pass
    

class Accounts(CRUD[Account]):
    def __init__(self):
        pass

    def register(self, username : str, password : SecretStr):
        account = self.read(username=username)
        if account is not None:
            raise Exception('Account already exists')
        
        self.create(username=username, password=password)

    def authenticate(self, username : str, password : SecretStr):
        account = self.read(username=username)
        if account is None:
            raise Exception('Account not found')
        
        account.authenticate(password)