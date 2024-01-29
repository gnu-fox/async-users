from abc import ABC, abstractmethod
from typing import Union

from src.users.domain.models import SecretStr

class Credentials(ABC):

    @abstractmethod
    async def verify(self, username: str, password: Union[str, SecretStr]) -> bool:
        ...

    @abstractmethod
    async def update(self,  username: str,  password: Union[str, SecretStr], new_password: Union[str, SecretStr]) -> bool:
        ...
