from uuid import uuid4
from typing import Protocol
from typing import Union
from typing import Set
from typing import Optional

from sqlalchemy import URL
from sqlalchemy import insert, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from users.domain.services import Security
from users.domain.entities import ID, Account
from users.domain.value_objects import Credentials
from users.domain.value_objects import UsernameAndPassword
from users.ports.repository import Accounts as Repository
from users.adapters.schemas import User
from users.settings import Settings


class SessionFactory(Protocol):
    def __call__(self) -> AsyncSession:
        ...

def create_session_factory(url: Union[str, URL]) -> SessionFactory:
    engine = create_async_engine(url)
    return async_sessionmaker(engine, expire_on_commit=False)


class Authentication:

    def __init__(self, session : AsyncSession):
        self.session = session

    async def register(self, credentials : Credentials) -> ID:
        user_id = uuid4()
        if isinstance(credentials, UsernameAndPassword):
            password = Security.hash(credentials.password)
            statement = insert(User).values(id = user_id, username = credentials.username, password = password)

        await self.session.execute(statement)
        return user_id
    
    async def authenticate(self, credentials : Credentials) -> ID:
        if isinstance(credentials, UsernameAndPassword):
            return await self.authenticate_with_username_and_password(credentials.username, credentials.password)
        
    async def delete(self, id : ID):
        statement = delete(User).where(User.id == id)
        await self.session.execute(statement)

    async def authenticate_with_username_and_password(self, username : str, password : str) -> ID:
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement)
        schema = result.scalars().first()
        if Security.verify(password, schema.password) is False:
            raise Exception("Invalid password")
        return schema.id


class Accounts(Repository):

    def __init__(self, settings : Settings):
        self.session_factory = create_session_factory(settings.database_url)
        self.seen : Set[Account] = set()
        self.removed : Set[Account] = set()

    async def __aenter__(self):
        self.session = self.session_factory()
        self.authentication = Authentication(session=self.session)
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()

    async def commit(self):
        self.collection.update(self.seen)
        self.collection.difference_update(self.removed)
        await self.session.commit()
        
    async def create(self, credentials : Credentials) -> Account:
        account_id = self.authentication.register(credentials)
        account = Account(id = account_id)
        self.seen.add(account)
        return account
    
    async def read(self, credentials : Credentials) -> Account:
        account_id = self.authentication.authenticate(credentials)
        account = Account(id = account_id)
        self.collection.add(account)
        return account
        
    async def delete(self, account : Account):
        self.authentication.delete(account.id)
        self.removed.add(account)