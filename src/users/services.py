from uuid import uuid4
from abc import ABC, abstractmethod
from typing import Union
from typing import TypeVar, Generic

from src.users.models import Event, Command
from src.users.models import User
from src.users.models import Account
from src.users.repository import Repository
from src.users.application import Application

T = TypeVar('T', bound=Union[Event, Command])
class Handler(ABC, Generic[T]):

    @abstractmethod
    async def call(self, message : T):
        ...

class CreateAccountHandler(Handler[Command]):
    def __init__(self, uow):
        self.uow = uow

    async def call(self, message : Command):
        print(f"creating account with {message}")


class AccountCreatedHandler(Handler[Event]):
    def __init__(self, uow):
        self.uow = uow

    async def call(self, message : Event):
        print(f"account created with {message}")