from uuid import uuid4
from typing import Union

from pydantic_settings import BaseSettings

from src.auth import exceptions
from src.auth.models.accounts import Account
from src.auth.models.credentials import Credentials 
from src.auth.adapters.adapters import UnitOfWork, URL

class Settings(BaseSettings):
    database_uri : Union[str, URL]    
    token_url : str = "/token"

class Authentication:
    def __init__(self, uow : UnitOfWork):
        self.uow = uow
    
    async def authenticate(self, **kwargs) -> Account:
        credentials = Credentials(**kwargs)
        async with self.uow as uow:
            account = await uow.accounts.read(credentials=credentials)
            if not account:
                raise exceptions.AccountNotFound
            
            if not account.verify(credentials):
                raise exceptions.InvalidCredentials
            return Account(id = account.id)
    
    async def register(self, **kwargs):
        credentials = Credentials(**kwargs)
        credentials.hash()

        async with self.uow as uow:
            account = await uow.accounts.read(credentials)
            if account:
                raise exceptions.AccountAlreadyExists
            
            await uow.accounts.create(account=Account(id=uuid4(), credentials=credentials))
            await uow.commit()