class AccountAlreadyExists(Exception):
    def __init__(self, *args, **kwargs):
        message = "Account already exists"
        super().__init__(message,  *args, **kwargs)

class AccountNotFound(Exception):
    def __init__(self, *args, **kwargs):
        message = "Account not found"
        super().__init__(message,  *args, **kwargs)

class InvalidCredentials(Exception):
    def __init__(self, *args, **kwargs):
        message = "Invalid credentials"
        super().__init__(message,  *args, **kwargs)