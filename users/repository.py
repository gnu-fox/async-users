from typing import Protocol
from typing import Optional
from typing import TypeVar

from users.models import Account
from users.models import User
from users.models import Credentials

class Accounts(Protocol):

    async def create(self, credentials : Credentials) -> Account:
        ...
    
    async def read(self, credentials : Credentials) -> Optional[Account]:
        ...

    async def delete(self, account : Account):
        ...

    async def update(self, account : Account, credentials : Credentials):
        ...
    
    async def verify(self, credentials : Credentials) -> bool:
        ...


class Users:
    def __init__(self, accounts : Accounts):
        self.accounts = accounts

    async def register(self, credentials : Credentials) -> User:
        created_account = await self.accounts.create(credentials)
        user = User(account = created_account)
        return user
    
    async def authenticate(self, credentials : Credentials) -> User:
        retrieved_account = await self.accounts.read(credentials)
        user = User(account = retrieved_account)
        return user