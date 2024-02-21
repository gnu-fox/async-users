from abc import ABC, abstractmethod
from uuid import uuid4
from typing import TypeVar, Generic
from typing import Union

from src.users.models import User
from src.users.models import Event, Command
from src.users.models import Account
from src.users.repository import Repository
from src.users.application import Application
from src.users.application import Factory
from src.users.ports import UnitOfWork
from src.users import events

from src.auth.services import register
from src.auth.models.credentials import Credential
from src.auth.adapters.adapters import SessionFactory
from src.auth.adapters.adapters import UnitOfWork as DefaultUnitOfWork


T = TypeVar('T', bound=Union[Event, Command])
class Handler(ABC, Generic[T]):

    @abstractmethod
    async def __call__(self, message : T):
        pass


class CreateAccount(Handler[events.UserCreated]):
    def __init__(self, uow : UnitOfWork):
        self.uow = uow

    async def __call__(self, event : events.UserCreated):
        credential = Credential(**event.model_dump())
        await register(credential=credential, uow=self.uow)


class Users:
    repository = Repository[User] = Repository(collection=set())

    @classmethod
    def attach(cls, user : User):
        cls.repository.add(user)

    def __init__(self, uow : UnitOfWork):
        self.uow = uow
        self.application = Application(self.repository)
        self.application.consumers[events.UserCreated] = [CreateAccount(uow=uow)]

    #TODO: FIX THIS, users should have it's own session factory

    async def __aenter__(self):
        await self.uow.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.uow.__aexit__(exc_type, exc, tb)

    async def create(self, **kwargs):
        id = uuid4()
        account = Account(id=id)
        user = User(account=account)
        user.dispatch(event=events.UserCreated(id=id, **kwargs))
        self.attach(user)
        return user
    
    async def read(self, **kwargs):
        account = await self.uow.accounts.read(Credential(**kwargs))
        if account:
            user = User(account=account)
            self.attach(user)
            return user