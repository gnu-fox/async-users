from typing import Any
from pydantic import BaseModel
from pydantic import SecretStr, EmailStr

class Credentials:
    username : str | None
    password : SecretStr | None

class Account:
    id : Any

class User:
    def __init__(self, account : Account):
        self.account = account

    @property
    def id(self):
        return self.account.id