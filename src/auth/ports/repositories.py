from src.auth.domain.aggregates import Account
from src.auth.ports.protocols import CRUD

class Accounts(CRUD[Account]):
    pass