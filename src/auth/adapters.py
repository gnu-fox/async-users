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

from src.auth.models import Account
from src.auth.models import Credentials, SecretStr
from src.auth.models import Security
from src.auth.schemas import ACCOUNT

class Accounts:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, account : Account, credentials : Credentials):
        if credentials.username and credentials.password:
            hash = Security.hash(credentials.password)
            command = insert(ACCOUNT).values(id=account.id, username=credentials.username, password=hash.get_secret_value())
            await self.session.execute(command)
        else:
            raise KeyError("Invalid credentials")    

    async def read(self, credentials : Credentials) -> Optional[Account]:
        if credentials.username:
            query = select(ACCOUNT).where(ACCOUNT.username == credentials.username)
        else:
            raise KeyError("Invalid credentials")
            
        result = await self.session.execute(query)
        account = result.scalars().first()

        if account:
            authenticated = Security.verify(credentials.password, account.password) if credentials.password else False
            return Account(id=account.id, authenticated = authenticated)

    async def update(self, account : Account, credentials : Credentials):
        command = update(ACCOUNT).where(ACCOUNT.id == account.id).values(credentials.fields)
        await self.session.execute(command)

    async def delete(self, account : Account):
        command = delete(ACCOUNT).where(ACCOUNT.id == account.id)
        await self.session.execute(command)

    async def verify(self, account : Account, password : SecretStr) -> bool:
        query = select(ACCOUNT).where(ACCOUNT.id == account.id)
        result = await self.session.execute(query)
        account = result.scalars().first()
        if account:
            return Security.verify(password, account.password)
        return False
    


class SessionFactory:
    def __init__(self, url : Union[str, URL]):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession)

    def __call__(self) -> AsyncSession:
        return self.session_factory()    
    

class UnitOfWork:
    def __init__(self, session_factory : SessionFactory):
        self.session_factory = session_factory

    async def begin(self):
        self.session = self.session_factory()
        await self.session.begin()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        await self.begin()
        return self
    
    async def __aexit__(self, exc_type : Any, exc_value : Any, traceback : Any):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()
