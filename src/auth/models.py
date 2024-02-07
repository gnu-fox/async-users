from typing import Any
from typing import TypeVar
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import RootModel
from pydantic import SecretStr, EmailStr

class Credentials(BaseModel):
    pass

class UsernameAndPassword(Credentials):
    username: str
    password: SecretStr

class EmailAndPassword(Credentials):
    email: EmailStr
    password: SecretStr

class ID(RootModel):
    root : Any

class Account(BaseModel):
    id : ID

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return False
        return self.id == other.id
    
    def __hash__(self) -> ID:
        return hash(self.id)
    
    model_config = ConfigDict(arbitrary_types_allowed = True)