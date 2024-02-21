from typing import Optional
from uuid import UUID
from pydantic import SecretStr
from pydantic import EmailStr

from src.users.models import Event

class UserCreated(Event):
    id : UUID
    username : Optional[str]
    password : Optional[SecretStr]
    email : Optional[EmailStr]