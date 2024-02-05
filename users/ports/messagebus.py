from typing import Set
from typing import Dict
from typing import List
from typing import Callable
from typing import Generator
from typing import Union
from collections import deque

from users.ports.repository import Repository
from users.domain.messages import Event, Command

class MessageBus:
    def __init__(self, repository : Repository):
        self.repository = repository
        self.event_handlers : Dict[Event, List[Callable]] = {}
        self.command_handlers : Dict[Command, Callable] = {}
        self.queue = deque()

    def handle(self, message : Union[Event, Command]):
        self.queue.append(message)
        
        while self.queue:
            message = self.queue.popleft()
            if isinstance(message, Event):
                self.handle_event(message)
            elif isinstance(message, Command):
                self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")
            

    def handle_event(self, event: Event):
        for handler in self.event_handlers[type(event)]:
            try:
                print(f"handling {event} event with {handler} handler")
                handler(event, self.repository)
                self.queue.extend(self.repository.collect_events())
            except Exception:
                print(f"Exception handling {event} event %s", )
                raise

    def handle_command(self, command: Command):
        print(f"handling command {command}")
        try:
            handler = self.command_handlers[type(command)]
            handler(command, self.repository)
            self.queue.extend(self.repository.collect_events())
        except Exception:
            print(f"Exception handling {command} command %s")
            raise