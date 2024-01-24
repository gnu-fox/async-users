from abc import ABC, abstractmethod
from typing import Deque, Set, List
from typing import Generator, TypeVar, Generic
from collections import deque

from src.messagebus.events import Event

class Aggregate(ABC):
    def __init__(self):
        self.events: Deque[Event] = deque()


T = TypeVar('T', bound=Aggregate)
class Repository(ABC, Generic[T]):
    def __init__(self):
        self.seen: Set[T] = set()


class Context(ABC):
    repositories: List[Repository[Aggregate]]

    def events(self) -> Generator[Event, None, None]:
        for repository in self.repositories:
            for aggregate in repository.seen:
                while aggregate.events:
                    yield aggregate.events.popleft()

        