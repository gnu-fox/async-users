from typing import Union
from pydantic import SecretStr

from src.users.ports.accounts import Accounts
from src.users.ports.credentials import Credentials

class Users:
    def __init__(self):
        self.accounts : Accounts
        self.credentials : Credentials

    async def create(self, username: str, password: Union[str, SecretStr]) -> None:
        await self.accounts.create(username, password)