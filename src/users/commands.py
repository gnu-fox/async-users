from uuid import uuid4
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

class Command(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    timestamp : datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(frozen=True)

class CreateUser(Command):
    username : str = Field(..., alias="username", description="The username of the Account")
    password : str = Field(..., alias="password", description="The password of the Account")
    email : str = Field(..., alias="email", description="The email of the Account")