from typing import Protocol
from typing import Optional

from src.auth.models.accounts import Account
from src.auth.models.credentials import Credential

class Accounts(Protocol):

    async def create(self, **kwargs):
        ...

    async def read(self, **kwargs) -> Optional[Account]:
        ...

    async def update(self, account : Account):
        ...

    async def delete(self, account : Account):
        ...


class UnitOfWork(Protocol):
    accounts : Accounts

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc, tb):
        ...

    async def commit(self):
        ...