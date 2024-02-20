from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr
from pydantic import EmailStr
from pydantic import field_serializer, field_validator

from src.auth.models.security import Security

class Credentials(BaseModel):
    username : str = Field(default=None, alias="username", description="The username of the Account")
    password : SecretStr = Field(default=None, alias="password", description="The password of the Account")
    email : EmailStr = Field(default=None, alias="email", description="The email of the Account")

    @field_serializer('password', when_used='always')
    def reveal(password : SecretStr) -> str:
        return password.get_secret_value()
    
    def hash(self):
        self.password = Security.hash(self.password)

    def verify(self, password : Union[str, SecretStr]) -> bool:
        return Security.verify(password, self.password)