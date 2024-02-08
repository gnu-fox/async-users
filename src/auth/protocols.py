from typing import Protocol
from typing import Optional
from typing import Dict
from typing import TypeVar
from typing import Any

class Cryptography(Protocol):

    def hash(self, password : str) -> str:
        ...

    def verify(self, password : str, hash : str) -> bool:
        ...        
        

ID = TypeVar("ID")
class Accounts(Protocol[ID]):
    
    async def create(self, credentials : Dict[str, Any]) -> ID:
        ...

    async def read(self, credentials : Dict[str, Any]) -> Optional[ID]:
        ...
    
    async def verify(self, credentials : Dict[str, Any]) -> bool:
        ...

    async def update(self, id : ID, credentials : Dict[str, Any]):
        ...
    
    async def delete(self, id : ID):
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