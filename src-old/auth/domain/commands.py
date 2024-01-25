from uuid import UUID
from typing import Union, Literal

from pydantic.dataclasses import dataclass

from src.messagebus import Command, Payload
from src.auth.domain.models import ID, SecretStr

@dataclass
class Authenticate(Payload):
    username : str
    password : SecretStr

@dataclass
class Register(Payload):
    username : str
    password : SecretStr