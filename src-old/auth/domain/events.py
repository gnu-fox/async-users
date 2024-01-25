from typing import Literal

from pydantic.dataclasses import dataclass

from src.messagebus import Event, Payload
from src.auth.domain.models import ID

@dataclass
class Authenticated(Payload):
    id : ID
    username : str
    status : Literal['success', 'failed']