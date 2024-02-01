from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar, Generator
from typing import Set

from src.ddd.ports import Context
from src.ddd.domain import Aggregate, Event

T = TypeVar('T', bound=Aggregate)
class Repository(ABC, Generic[T]):
    def __init__(self):
        self.__seen : Set[T] = set()

    @property
    def events(self) -> Generator[Event, None, None]:
        for aggregate in self.__seen:
            while aggregate.events:
                yield aggregate.events.popleft()

    def listen(self, aggregate : T) -> T:
        self.__seen.add(aggregate)
        return aggregate