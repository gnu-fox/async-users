from typing import Any
from typing import Deque
from typing import Generator

from collections import deque
from uuid import UUID
from pydantic import BaseModel


class Event(BaseModel):
    pass


class Command(BaseModel):
    pass


class Entity(BaseModel):
    id : Any

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, self.__class__):
            return self.id == __value.id
        return False
    
    def __hash__(self) -> int:
        return hash(self.id)


class Aggregate:
    def __init__(self, root : Entity):
        self.__id = root.id
        self.events : Deque[Event] = deque()
        self.saved = False

    @property
    def id(self) -> Any:
        return self.__id
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, self.__class__):
            return self.id == __value.id
        return False
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def dispatch(self, event : Event):
        self.events.append(event)
    
    def save(self):
        self.saved = True
    
    def discard(self):
        self.events.clear()
        self.saved = False


class Account(Entity):
    id : UUID


class User(Aggregate):
    def __init__(self, account : Account):
        super().__init__(root=account)