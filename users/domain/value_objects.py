from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import SecretStr, EmailStr

class ValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)

class Credentials(ValueObject):
    pass

class UsernameAndPassword(Credentials):
    username: str
    password: SecretStr

class EmailAndPassword(Credentials):
    email: EmailStr
    password: SecretStr