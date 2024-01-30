from typing import Union
from pydantic import SecretStr

from src.users.ports.accounts import Accounts
from src.users.ports.credentials import Credentials
from src.users.ports.utils import Repository

from src.users.domain.models import User

class Users(Repository):
    def __init__(self):
        self.accounts : Accounts
        self.credentials : Credentials

    async def create(self, username: str, password: Union[str, SecretStr]) -> User:
        raise NotImplementedError
    
    