from src.auth.domain.models import ID

class Account:
    def __init__(self, id : ID, username : str):
        self.id = id
        self.username = username