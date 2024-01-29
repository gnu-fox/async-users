from abc import ABC, abstractmethod
from typing import Union

from src.users.domain.models import Account, SecretStr, ID

class Accounts(ABC):

    @abstractmethod
    async def create(self, username: str, password: Union[str, SecretStr]) -> None:
        ...

    @abstractmethod
    async def read(self, **kwargs) -> Union[Account, None]:
        ...

    @abstractmethod
    async def update(self, id: ID, username: str) -> None:
        ...

    @abstractmethod
    async def delete(self, id: ID) -> None:
        ...


class Credentials(ABC):

    @abstractmethod
    async def verify(self, username: str, password: Union[str, SecretStr]) -> bool:
        ...

    @abstractmethod
    async def update(self,  username: str,  password: Union[str, SecretStr], new_password: Union[str, SecretStr]) -> bool:
        ...

