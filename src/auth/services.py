from uuid import uuid4

from src.auth import exceptions
from src.auth.models.accounts import Account
from src.auth.models.credentials import Credential 
from src.auth.adapters.adapters import UnitOfWork

async def authenticate(credential : Credential, uow : UnitOfWork) -> Account:
    async with uow:
        account = await uow.accounts.read(credential=credential)
        if not account:
            raise exceptions.AccountNotFound
        
        if not account.verify(credential):
            raise exceptions.InvalidCredential
        return Account(id = account.id)
    

async def register(credential : Credential, uow : UnitOfWork):
    credential.hash()
    async with uow:
        account = await uow.accounts.read(credential)
        if account:
            raise exceptions.AccountAlreadyExists
        
        await uow.accounts.create(account=Account(id=credential.id if credential.id else uuid4(), credential=credential))