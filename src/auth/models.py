from typing import Any
from typing import Optional
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import RootModel
from pydantic import SecretStr, EmailStr

class Credentials(BaseModel):
    username: Optional[str]
    password: Optional[SecretStr]
    email: Optional[EmailStr]

class Account(RootModel):
    root : Any
