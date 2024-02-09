from typing import Protocol
from typing import Optional
from typing import TypeVar

from src.users.models import Account
from src.users.models import User

ID = TypeVar("ID")
class Accounts(Protocol[ID]):
    
    async def create(self, **kwargs) -> ID:
        ...

    async def read(self, **kwargs) -> Optional[ID]:
        ...

    async def update(self, id : ID, **kwargs):
        ...

    async def delete(self, id : ID):
        ...

class Users:
    def __init__(self, accounts : Accounts):
        self.accounts = accounts

    async def create(self, **kwargs) -> User:
        account = await self.accounts.create(**kwargs)
        return User(account)
    
    async def read(self, **kwargs) -> Optional[User]:
        account = await self.accounts.read(**kwargs)
        if account:
            return User(account)
        
    async def delete(self, user : User):
        await self.accounts.delete(user.account)