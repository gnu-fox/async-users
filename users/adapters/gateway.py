from uuid import UUID
from uuid import uuid4
from typing import Optional
from typing import Dict
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from users.adapters.schemas import Account

class Accounts:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, credentials : Dict[str, Any]) -> UUID:
        ...

    async def read(self, credentials : Dict[str, Any]) -> Optional[UUID]:
        ...

    async def delete(self, id : UUID):
        ...

    async def verify(self, credentials : Dict[str, Any]) -> bool:
        ...
    
    async def update(self, id : UUID, credentials : Dict[str, Any]):
        ...
