from uuid import UUID

from src.messagebus import Entity, Aggregate
from src.messagebus import Repository

class Account(Entity):
    id : UUID

class User(Aggregate):
    def __init__(self, account : Account):
        super().__init__(root=account)
        self.account = account

class Users(Repository[User]):
    def __init__(self):
        super().__init__()