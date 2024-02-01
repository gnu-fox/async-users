from typing import TypeVar
from typing import Deque
from collections import deque

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

class Event:
    pass

ID = TypeVar('ID')

class Entity(BaseModel):
    id : ID

class Aggregate:
    def __init__(self, root : Entity):
        self.id : ID = root.id
        self.events : Deque[Event] = deque()

    def __eq__(self, other):
        return isinstance(other, Aggregate) and self.id == other.id