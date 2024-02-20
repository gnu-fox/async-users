from typing import Protocol
from typing import Union

from pydantic import SecretStr
from passlib.context import CryptContext

class Cryptography(Protocol):

    def hash(self, password : str) -> str:
        ...

    def verify(self, password : str, hash : str) -> bool:
        ...

def reveal(secret : Union[str, SecretStr]) -> str:
    if isinstance(secret, SecretStr):
        return secret.get_secret_value()
    return secret


class Security:
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password : Union[str, SecretStr]) -> SecretStr:
        return SecretStr(cls.context.hash(reveal(password)))
    
    @classmethod
    def verify(cls, password : Union[str, SecretStr], hash : Union[str, SecretStr]) -> bool:
        if not password or not hash:
            return False
        
        return cls.context.verify(secret = reveal(password), hash = reveal(hash))