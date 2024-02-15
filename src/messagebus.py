from uuid import uuid4
from uuid import UUID
from abc import ABC, abstractmethod
from typing import Optional
from typing import Union
from typing import Dict, Deque, Set, Any, List
from typing import Generator
from typing import TypeVar
from typing import Generic
from collections import deque
from datetime import datetime

from pydantic import RootModel
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

class Message(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    timestamp : datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(frozen=True)

class Event(Message):
    type : str = Field(..., alias="type", description="The type of the Event")
    payload : Any

class Command(Message):
    type : str = Field(..., alias="type", description="The type of the Command")
    payload : Any


class ID(RootModel):
    root : Any

class ValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)


class Entity(BaseModel):
    id : ID

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id if isinstance(__value, self.__class__) else False
    
    def __hash__(self) -> int:
        return hash(self.id)


class Aggregate:
    def __init__(self, root : Entity):
        self.__identifier = root.id.root if isinstance(root.id, RootModel) else root.id
        self.events : Deque[Event] = deque()
        self.saved = False

    @property
    def id(self):
        return self.__identifier

    def save(self):
        self.saved = True

    def discard(self):
        self.events.clear()

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id if isinstance(__value, self.__class__) else False
    
    def __hash__(self) -> int:
        return hash(self.id)
    

T = TypeVar('T', bound=Aggregate, covariant=True)
class Repository(Generic[T]):
    
    def __init__(self, collection : Set[T] = set()):
        self.collection : Set[T] = collection

    def add(self, aggregate : T):
        self.collection.add(aggregate)
    
    def get(self, id) -> Optional[T]:
        for aggregate in self.collection:
            if aggregate.id == id:
                return aggregate
        return None

    def remove(self, aggregate : T):
        self.collection.remove(aggregate)

    @property
    def events(self) -> Generator[Event, None, None]:
        for aggregate in self.collection:
            if aggregate.saved:
                while aggregate.events:
                    yield aggregate.events.popleft()
            aggregate.saved = False

MSG = TypeVar('MSG', bound=Union[Event, Command])
class Handler(ABC, Generic[MSG]):
    @abstractmethod
    async def __call__(self, message : MSG):
        ...

class Application:
    def __init__(self, repository : Repository):
        self.repository = repository
        self.queue = deque()
        self.publishers : Dict[str, Handler[Command]] = {}
        self.consumers : Dict[str, List[Handler[Event]]] = {}

    async def handle(self, message : Union[Event, Command]):
        self.queue.append(message)

        while self.queue:
            message = self.queue.popleft()
            if isinstance(message, Event):
                await self.consume(message)
            elif isinstance(message, Command):
                await self.publish(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    async def consume(self, event: Event):
        for handler in self.consumers[event.type]:
            try:
                print(f"handling event {event} with handler {handler}")
                await handler(event)
                self.queue.extend(self.repository.events)
            except Exception:
                print(f"Exception handling event {event}")
                continue

    async def publish(self, command: Command):
        print(f"handling command {command}")
        try:
            handler = self.publishers[command.type]
            await handler(command)
            self.queue.extend(self.repository.events)
        except Exception:
            print(f"Exception handling command {command}")
            raise

    async def start(self):
        while True:
            message = self.queue.popleft()
            await self.handle(message)