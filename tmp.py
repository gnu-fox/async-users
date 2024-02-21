from src.users.models import User
from src.users.models import Account
from src.users.repository import Repository

class Factory:
    repository = Repository[User](collection=set())

    @classmethod
    def create(self, account : Account) -> User:
        user = User(account=account)
        self.repository.add(user)
        return user
    

users = Factory
account = Account(id=1)
user = users.create(account)
users.repository.add(user)
assert users.repository.get(1) == user