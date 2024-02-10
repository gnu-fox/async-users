from typing import Any
from pydantic import BaseModel
from pydantic import RootModel
from pydantic import SecretStr, EmailStr
from pydantic import Field

class ID(RootModel):
    root : Any

class Credentials(BaseModel):
    username : str = Field(None)
    password : SecretStr = Field(None)

class Account:
    def __init__(self, identity : ID):
        self.identity = identity

    @property
    def id(self):
        if isinstance(self.identity, RootModel):
            return self.identity.root
        else:
            return self.identity

    def __eq__(self, other):
        if isinstance(other, Account):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)