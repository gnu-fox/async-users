from abc import ABC, abstractmethod
from typing import Union, Protocol

from src.users.domain.models import SecretStr
from src.users.ports.utils import DataAccessObject as DAO

class Credentials(Protocol):

    async def verify(self, username: str, password: Union[str, SecretStr]) -> bool:
        ...

    async def update(self,  username: str,  password: Union[str, SecretStr], new_password: Union[str, SecretStr]) -> bool:
        ...