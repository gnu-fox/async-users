from uuid import UUID, uuid4
from datetime import datetime
from abc import ABC
from collections import deque
from typing import Type, TypeVar, Generic
from typing import Deque

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

@dataclass
class Payload(ABC):
    pass

T = TypeVar('T', bound=Payload)
class Command(BaseModel, Generic[T]):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now)
    payload: T
    
    @property
    def type(self) -> Type[T]:
        return type(self.payload)


T = TypeVar('T', bound=Payload)
class Event(BaseModel, Generic[T]):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now)
    payload: T
    
    @property
    def type(self) -> Type[T]:
        return type(self.payload)
    

class Aggregate(ABC):
    def __init__(self):
        self.events: Deque[Event] = deque()

    def publish(self, event: Event):
        self.events.append(event)