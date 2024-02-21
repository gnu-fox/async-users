from uuid import uuid4
from typing import Dict
from typing import Deque
from typing import Callable
from typing import List
from typing import Union
from collections import deque

from src.users.models import User, Account
from src.users.models import Event, Command
from src.users.repository import Repository

class Application:
    def __init__(self, repository : Repository):
        self.repository = repository
        self.publishers : Dict[Event, Callable[[Command], None]] = {}
        self.consumers : Dict[Event, List[Callable[[Event], None]]] = {}
        self.queue = deque()

    async def handle(self, message : Union[Event, Command]):
        self.queue.append(message)
        while self.queue:
            message = self.queue.popleft()
            if isinstance(message, Command):
                await self.publish(message)
            elif isinstance(message, Event):
                await self.consume(message)

    async def publish(self, command: Command):
        try:
            await self.publishers[type(command)](command)
            self.queue.extend(self.repository.collect_events())
        except Exception:
            raise
    
    async def consume(self, event: Event):
        for handler in self.consumers[type(event)]:
            try:
                await handler(event)
                self.queue.extend(self.repository.collect_events())
            except Exception:
                continue

class Factory:
    repository = Repository[User](collection=set())

    @classmethod
    def create(self, account : Account) -> User:
        user = User(account=account)
        self.repository.add(user)
        return user
    
class Users:
    def __init__(self):
        self.factory = Factory
        self.application = Application(self.factory.repository)

    async def create(self, **kwargs) -> User:
        user = self.factory.create(Account(id = uuid4()))
        return user
