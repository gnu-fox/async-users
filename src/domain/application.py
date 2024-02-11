from abc import ABC, abstractmethod
from typing import Dict
from typing import List
from typing import Union
from typing import TypeVar, Generic
from collections import deque

from src.domain.messages import Event, Command
from src.domain.repository import Repository

MSG = TypeVar('MSG', bound=Union[Event, Command])
class Handler(ABC, Generic[MSG]):
    @abstractmethod
    async def __call__(self, message : MSG):
        ...

class Application:
    def __init__(self, repository : Repository):
        self.repository = repository
        self.queue = deque()
        self.publishers : Dict[Command, Handler[Command]] = {}
        self.consumers : Dict[Event, List[Handler[Event]]] = {}

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
        for handler in self.consumers[type(event)]:
            try:
                print(f"handling event {event} with handler {handler}")
                await handler(event)
                self.queue.extend(self.repository.events)
            except Exception:
                print(f"Exception handling event {event}")
                raise

    async def publish(self, command: Command):
        print(f"handling command {command}")
        try:
            handler = self.publishers[type(command)]
            await handler(command)
            self.queue.extend(self.repository.events)
        except Exception:
            print(f"Exception handling command {command}")
            raise