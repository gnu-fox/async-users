from typing import Protocol
from typing import Optional
from typing import Dict
from typing import TypeVar
from typing import Any

from src.auth.models import Account

class Cryptography(Protocol):

    def hash(self, password : str) -> str:
        ...

    def verify(self, password : str, hash : str) -> bool:
        ...


class Accounts(Protocol):
    
    async def create(self, credentials : Dict[str, Any]) -> Account:
        ...

    async def read(self, credentials : Dict[str, Any]) -> Optional[Account]:
        ...
    
    async def verify(self, credentials : Dict[str, Any]) -> bool:
        ...

    async def update(self, account : Account, credentials : Dict[str, Any]):
        ...
    
    async def delete(self, account : Account):
        ...


class Session(Protocol):

    async def begin(self):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def close(self):
        ...