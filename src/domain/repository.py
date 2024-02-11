from typing import Set
from typing import Generator
from typing import Optional
from typing import TypeVar, Generic

from src.domain.models import Event
from src.domain.models import Aggregate
from src.domain.models import Account
from src.domain.models import User
from src.domain.messages import Event

T = TypeVar('T', bound=Aggregate, covariant=True)
class Repository(Generic[T]):
    def __init__(self):
        self.__collection : Set[T]  = set()

    def add(self, aggregate : Aggregate):
        self.__collection.add(aggregate)
    
    def get(self, id) -> Optional[Aggregate]:
        for aggregate in self.__collection:
            if aggregate.id == id:
                return aggregate

    def remove(self, aggregate : Aggregate):
        self.__collection.remove(aggregate)
    
    @property
    def collection(self) -> Set[Aggregate]:
        return self.__collection

    @property
    def events(self) -> Generator[Event, None, None]:
        for aggregate in self.collection:
            while aggregate.events:
                yield aggregate.events.popleft()
