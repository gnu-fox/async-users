from abc import ABC, abstractmethod
from typing import Union, Protocol

from src.users.domain.models import Account, SecretStr, ID
from src.users.ports.utils import DataAccessObject as DAO

class Accounts(Protocol):

    async def create(self, username: str, password: Union[str, SecretStr]) -> None:
        ...

    async def read(self, **kwargs) -> Union[Account, None]:
        ...

    async def update(self, id: ID, username: str) -> None:
        ...

    async def delete(self, id: ID) -> None:
        ...