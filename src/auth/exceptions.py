class AccountAlreadyExists(Exception):
    def __init__(self, *args, **kwargs):
        message = "Account already exists"
        super().__init__(message,  *args, **kwargs)

class AccountNotFound(Exception):
    def __init__(self, *args, **kwargs):
        message = "Account not found"
        super().__init__(message,  *args, **kwargs)

class InvalidCredential(Exception):
    def __init__(self, *args, **kwargs):
        message = "Invalid credential"
        super().__init__(message,  *args, **kwargs)