from uuid import uuid4
from uuid import UUID
from typing import Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.schemas import Account
from src.backend.security import Security

class Accounts:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.security = Security()

    async def create(self, **kwargs) -> UUID:
        account_id = uuid4()
        if 'password' in kwargs:
            kwargs['password'] = self.security.hash(kwargs['password'])

        statement = insert(Account).values(id=account_id, **kwargs)
        await self.session.execute(statement)
        return account_id

    async def read(self, **kwargs) -> Optional[UUID]:
        key, value = kwargs.popitem()
        statement = select(Account).where(getattr(Account, key) == value)
        result = await self.session.execute(statement)
        account = result.scalars().first()
        if account:
            return account.id

    async def update(self, id : UUID, **kwargs) -> None:
        statement = update(Account).where(Account.id == id).values(**kwargs)
        await self.session.execute(statement)

    async def delete(self, id : UUID) -> None:
        statement = delete(Account).where(Account.id == id)
        await self.session.execute(statement)

    async def verify(self, id : UUID, password : str) -> bool:
        statement = select(Account).where(Account.id == id)
        result = await self.session.execute(statement)
        account = result.scalars().first()
        return self.security.verify(password, account.password)