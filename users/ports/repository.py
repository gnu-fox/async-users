from abc import ABC, abstractmethod
from typing import Set
from typing import Generator

from users.domain.messages import Event
from users.domain.entities import ID, Account
from users.domain.value_objects import Credentials

class Repository(ABC):
    collection : Set[Account]

    def collect_events(self) -> Generator[Event, None, None]:
        for account in self.collection:
            while account.events:
                yield account.events.popleft()


class Accounts(Repository):

    @abstractmethod
    def create(self, credentials : Credentials) -> Account:
        pass
    
    @abstractmethod
    def read(self, credentials : Credentials) -> Account:
        pass

    @abstractmethod
    def delete(self, account : Account):
        pass