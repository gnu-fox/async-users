from typing import Deque
from typing import Set
from typing import Optional
from typing import Generator
from collections import deque

from src.users.accounts import Account
from src.users.accounts import Credential
from src.users.events import Event

class User:
    def __init__(self, root : Account):
        self.__identifier = root.id
        self.events : Deque[Event] = deque()
        self.saved = False

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id if isinstance(__value, self.__class__) else False
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    @property
    def id(self):
        return self.__identifier
    
    def save(self):
        self.saved = True

    def discard(self):
        self.events.clear()


class Repository:
    
    def __init__(self, collection : Set[User] = set()):
        self.collection : Set[User] = collection

    def add(self, user : User):
        self.collection.add(user)
    
    def get(self, id) -> Optional[User]:
        for user in self.collection:
            if user.id == id:
                return user
        return None

    def remove(self, user : User):
        self.collection.remove(user)

    @property
    def events(self) -> Generator[Event, None, None]:
        for user in self.collection:
            if user.saved:
                while user.events:
                    yield user.events.popleft()
            user.saved = False

class Users:
    repository = Repository(collection=set())
    
    @classmethod
    def attach(cls, user : User):
        cls.repository.add(user)

    async def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.attach(user)
        return user




    