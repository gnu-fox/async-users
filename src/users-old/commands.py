from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import SecretStr

class Command(BaseModel):
    model_config = ConfigDict(frozen=True)

class CreateUser(Command):
    username : str = Field(default=None, alias="username", description="The username of the Account")
    password : SecretStr = Field(default=None, alias="password", description="The password of the Account")
    email : str = Field(default=None, alias="email", description="The email of the Account")