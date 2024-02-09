from typing import Any
from pydantic import BaseModel
from pydantic import RootModel
from pydantic import SecretStr, EmailStr
from pydantic import Field

class Account(BaseModel):
    id : Any

class User:
    def __init__(self, account : Account):
        self.account = account

    def __eq__(self, other):
        if isinstance(other, User):
            return self.account == other.account
    
    def __hash__(self):
        return hash(self.account)