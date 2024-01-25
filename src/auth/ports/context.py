from src.auth.domain.aggregates import Account, ID
from auth.ports.protocols import ORM

class Users:
    def __init__(self, orm : ORM):
        self.__orm = orm
        self.accounts = orm.repositories['accounts']

    async def __aenter__(self):
        session = self.__orm.session
        await session.begin()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.accounts.session.rollback()
        await self.accounts.session.close()

    async def commit(self):
        await self.accounts.session.commit()