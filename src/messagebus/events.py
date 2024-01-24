from uuid import UUID, uuid4
from datetime import datetime
from abc import ABC
from typing import Type, TypeVar, Generic

from pydantic import BaseModel, Field

class Payload(ABC, BaseModel):
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
    