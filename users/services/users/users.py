from users.settings import Settings
from users.adapters.repository import Accounts

class Users:
    def __init__(self, settings : Settings):
        self.settings = settings
        self.repository = Accounts(settings)
        self.messagebus = MessageBus(self.repository)

    async def create(self, credentials : Credentials) -> User:
        account = await self.repository.create(credentials)
        return User(account)
    
    async def read(self, credentials : Credentials) -> User:
        account = await self.repository.read(credentials)
        return User(account)
    
    async def __aenter__(self):
        await self.repository.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.repository.__aexit__(exc_type, exc_value, traceback)
        await self.repository.commit()
        
