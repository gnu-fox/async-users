from abc import ABC, abstractmethod
from typing import Union
from typing import Dict
from typing import Deque
from typing import Callable
from typing import Generator
from typing import List
from typing import Set
from collections import deque

class Event:
    pass

class Command:
    pass

class Repository(ABC):

    @abstractmethod
    def collect_events(self) -> Generator[Event, None, None]:
        ...

class MessageBus:
    def __init__(self, repository: Repository):
        self.repository = repository
        self.event_handlers : Dict[type[Event], List[Callable]] = {}
        self.command_handlers : Dict[type[Command], Callable] = {}

    def handle(self, message: Union[Event, Command]):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Event):
                self.handle_event(message)
            elif isinstance(message, Command):
                self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    def handle_event(self, event: Event):
        for handler in self.event_handlers[type(event)]:
            try:
                print(f"handling event {event} with handler {handler}")
                handler(event)
                self.queue.extend(self.repository.collect_events())
            except Exception:
                print(f"Exception handling event {event}")
                continue

    def handle_command(self, command: Command):
        print(f"handling command {command}")
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.repository.collect_events())
        except Exception:
            print(f"Exception handling command {command}")
            raise

class Application:
    def __init__(self):
        self.message_bus = MessageBus