from typing import Union
from typing import Optional
from typing import Protocol
from typing import Dict
from typing import TypeVar
from typing import Any
from abc import ABC
from abc import abstractmethod

from pydantic import SecretStr

from src.auth.models import Account
from src.auth.models import Credentials
from src.auth.protocols import Cryptography
from src.auth.protocols import Accounts

def reveal(secret : Union[str, SecretStr]) -> str:
    if isinstance(secret, SecretStr):
        secret = secret.get_secret_value()
    return secret

class Security:
    def __init__(self, context : Cryptography): 
        self.context = context

    def hash(self, password : Union[str, SecretStr]) -> str:
        return self.context.hash(reveal(password))
    
    def verify(self, password : Union[str, SecretStr], hash : str) -> bool:
        return self.context.verify(reveal(password), hash)


class Repository(ABC):
    def __init__(self, accounts : Accounts):
        self.accounts = accounts

    async def create(self, credentials : Credentials) -> Account:
        root = await self.accounts.create(credentials.model_dump())
        account = Account(root = root)
        return account
    
    async def delete(self, account : Account):
        await self.accounts.delete(account.root)


