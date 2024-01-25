from typing import Callable

from src.messagebus import Aggregate, Event

from src.auth.domain.models import ID, SecretStr
from src.auth.domain.events import (
    Authenticated
)

class Account(Aggregate):
    def __init__(self, id : ID, username : str):
        self.id = id
        self.username = username
        self.verify : Callable[[SecretStr], bool] = lambda password : False

    def authenticate(self, password : SecretStr):
        status = 'success' if self.verify(password) else 'failed'
        payload = Authenticated(id=self.id, username=self.username, status=status)
        self.publish(event = Event(payload=payload))
        
