from uuid import uuid4
from uuid import UUID
from typing import Optional
from typing import Union
from typing import Any

from sqlalchemy import URL
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.adapters.schemas import ACCOUNT
from src.auth.models.credentials import Credential
from src.auth.models.accounts import Account

class Accounts:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, account : Account):
        credential = account.credential
        if credential.username and credential.password:
            command = insert(ACCOUNT).values(id=account.id, **credential.model_dump(exclude_none=True))
            await self.session.execute(command)
        else:
            raise KeyError("Invalid credential")    

    async def read(self, credential : Credential) -> Optional[Account]:
        if credential.username:
            query = select(ACCOUNT).where(ACCOUNT.username == credential.username)
        else:
            raise KeyError("Invalid credential")
            
        result = await self.session.execute(query)
        account = result.scalars().first()

        if account:
            credential = Credential(
                username=account.username, 
                password=account.password)
            return Account(id=account.id, credential=credential)

    async def update(self, account : Account):
        command = update(ACCOUNT).where(ACCOUNT.id == account.id).values(**account.credential.model_dump(exclude_none=True))
        await self.session.execute(command)

    async def delete(self, account : Account):
        command = delete(ACCOUNT).where(ACCOUNT.id == account.id)
        await self.session.execute(command)


class SessionFactory:
    def __init__(self, url : Union[str, URL]):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession)

    def __call__(self) -> AsyncSession:
        return self.session_factory()    


class UnitOfWork:
    def __init__(self, session_factory : SessionFactory):
        self.session_factory = session_factory

    async def commit(self):
        await self.session.commit()

    async def __aenter__(self):
        self.session = self.session_factory()
        self.accounts = Accounts(session=self.session)
        await self.session.begin()
        return self
    
    async def __aexit__(self, exc_type : Any, exc_value : Any, traceback : Any):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()