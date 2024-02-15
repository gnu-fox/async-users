import secrets
from uuid import UUID
from datetime import datetime, timedelta

from typing import Any
from typing import Dict
from typing import Protocol
from typing import Union
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import SecretStr, EmailStr
from pydantic import field_validator
from pydantic_settings import BaseSettings

from sqlalchemy import URL
from passlib.context import CryptContext

from jose import jwt
from jose import JWTError
from jose import ExpiredSignatureError

class Cryptography(Protocol):

    def hash(self, password : str) -> str:
        ...

    def verify(self, password : str, hash : str) -> bool:
        ...

def reveal(secret : Union[str, SecretStr]) -> str:
    if isinstance(secret, SecretStr):
        secret = secret.get_secret_value()
    return secret


class Security:
    context : Cryptography = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password : Union[str, SecretStr]) -> SecretStr:
        return SecretStr(cls.context.hash(reveal(password)))
    
    @classmethod
    def verify(cls, password : Union[str, SecretStr], hash : Union[str, SecretStr]) -> bool:
        if not password or not hash:
            return False
        return cls.context.verify(reveal(password), reveal(hash))    
    

class Credentials(BaseModel):
    username : Optional[str] = Field(None, description='The username of the account')
    password : Optional[SecretStr] = Field(None, description='The password of the account')

    @property
    def fields(self):
        dumped = self.model_dump(exclude_none=True)
        try:
            dumped['password'] = reveal(dumped['password'])
        except KeyError:
            pass

        return dumped
    
    model_config = ConfigDict(frozen=True)


class Claim(BaseModel):
    sub : str = Field(None, description='The subject of the token')
    exp : datetime = Field(
        default_factory = lambda: datetime.utcnow() + timedelta(minutes=15),
        description='The expiration of the token')
    
    @field_validator('sub', mode='before')
    @classmethod
    def to_string(cls, raw : Union[str,UUID]) -> str:
        if isinstance(raw, UUID):
            return str(raw)
        return raw
    
    @field_validator('exp', mode='before')
    @classmethod
    def to_datetime(cls, raw : Union[datetime, timedelta]) -> datetime:
        if isinstance(raw, timedelta):
            return datetime.utcnow() + raw
        return raw
    

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Tokenizer:
    secret : SecretStr = SecretStr(secrets.token_hex(16))

    @classmethod
    def encode(cls, claim : Claim, algorithm : str = 'HS256') -> Token:
        encoded_token = jwt.encode(claim.model_dump() , cls.secret.get_secret_value(), algorithm = algorithm)
        return Token(access_token = encoded_token, token_type = 'bearer')

    @classmethod
    def decode(cls, token : Token) -> Dict:
        try:
            decoded_token = jwt.decode(token.access_token, cls.secret.get_secret_value(), algorithms = ['HS256'])
            return decoded_token
        
        except ExpiredSignatureError as expired_error:
            raise ValueError("Token has expired") from expired_error
        
        except JWTError as jwt_error:
            raise ValueError("Invalid token") from jwt_error
        

class Account(BaseModel):
    id : UUID = Field(..., description='The unique identifier of the account')
    authenticated : bool = Field(False, description='The verification status of the account')

    def create_token(self, timedelta : timedelta = timedelta(minutes=15)) -> Token:
        if self.authenticated:
            claim = Claim(sub=self.id, exp=timedelta)
            return Tokenizer.encode(claim=claim)