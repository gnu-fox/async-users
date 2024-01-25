import logging
from abc import ABC
from typing import Dict, List, Callable, Union

from messagebus.domain import Event, Command
from messagebus.ports import Context

class Application(ABC):

    def __init__(self, context: Context):
        self.context = context
        self.event_handlers: Dict[type, List[Callable]]
        self.command_handlers: Dict[type, Callable]

    def handle(self, message : Union[Event, Command]):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Event):
                self.handle_event(message)

            elif isinstance(message, Command):
                self.handle_command(message)

            else:
                raise Exception(f'{message} was not an Event or Command')
            
    def handle_event(self, event : Event):
        for handler in self.event_handlers[event.type]:
            try:
                handler(event)
                self.queue.extend(self.context.events)
            except Exception:
                continue

    def handle_command(self, command : Command):
        try:
            handler = self.command_handlers[command.type]
            handler(command)
            self.queue.extend(self.context.events)
        except Exception:
            raise