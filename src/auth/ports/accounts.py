from typing import Protocol

from src.auth.models import Account, ID
from src.auth.models import Credentials

class Authentication(Protocol):

    async def register(self, credentials : Credentials) -> Account:
        ...

    async def retrieve(self, credentials : Credentials) -> Account:
        ...

    