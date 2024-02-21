from uuid import uuid4

from src.auth import exceptions
from src.auth.models.accounts import Account
from src.auth.models.credentials import Credentials 
from src.auth.adapters.adapters import UnitOfWork, URL

async def authenticate(credentials : Credentials, uow : UnitOfWork) -> Account:
    async with uow:
        account = await uow.accounts.read(credentials=credentials)
        if not account:
            raise exceptions.AccountNotFound
        
        if not account.verify(credentials):
            raise exceptions.InvalidCredentials
        return Account(id = account.id)

async def register(credentials : Credentials, uow : UnitOfWork):
    credentials.hash()
    async with uow:
        account = await uow.accounts.read(credentials)
        if account:
            raise exceptions.AccountAlreadyExists
        
        await uow.accounts.create(account=Account(id=uuid4(), credentials=credentials))
        await uow.commit()