from abc import ABC, abstractmethod
from typing import Deque, Set, List
from typing import Generator, TypeVar, Generic

from messagebus.domain import Event, Aggregate

T = TypeVar('T', bound=Aggregate)
class Repository(ABC, Generic[T]):
    def __init__(self):
        self.seen: Set[T] = set()

class Context(ABC):
    
    def __init__(self, repositories: List[Repository[Aggregate]]):
        self.repositories: List[Repository[Aggregate]] = repositories

    @property
    def events(self) -> Generator[Event, None, None]:
        for repository in self.repositories:
            for aggregate in repository.seen:
                while aggregate.events:
                    yield aggregate.events.popleft()