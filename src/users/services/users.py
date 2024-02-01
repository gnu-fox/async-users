from src.ddd.ports import Context
from src.ddd.domain import Aggregate

from src.users.domain.models import Account

from src.users.adapters.accounts import Accounts
from src.users.adapters.credentials import Credentials
from src.users.adapters.orm import ORM
from src.users.domain.models import User

class User(Aggregate):
    def __init__(self, account : Account):
        super().__init__(account)
        self.account = account

    @property
    def username(self):
        return self.account.username

    
        
class Users(Context):
    def __init__(self, orm : ORM):
        super().__init__(orm.session_factory)
        self.accounts = Accounts()
        self.credentials = Credentials()

    async def create(self, username : str, password : str):
        print("Creating user")
        account = await self.accounts.create(username = username, password = password)
        print("account created with username", account.username)
        return User(account)

    async def read(self, username : str):
        account = await self.accounts.read(username = username)
        return User(account)
    
    async def delete(self, username : str):
        account = await self.accounts.read(username = username)
        await self.accounts.delete(id = account.id)