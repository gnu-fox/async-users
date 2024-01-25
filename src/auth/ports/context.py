from src.auth.domain.aggregates import Account, ID
from src.auth.ports.protocols import ORM, CRUD, UOW

class Users(UOW):
    def __init__(self, orm : ORM):
        super().__init__(orm)
        self.accounts : CRUD[Account] = orm.repositories['accounts']