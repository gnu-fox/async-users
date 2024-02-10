import secrets
from typing import Union, Any
from typing import Dict
from datetime import datetime, timedelta

from jose import jwt
from jose import JWTError
from jose import ExpiredSignatureError
from pydantic import BaseModel
from pydantic import SecretStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class JWT:
    secret : str = secrets.token_hex(16)
    algorithm : str = "HS256"
    expires_delta : timedelta = timedelta(minutes=15)

    @classmethod
    def encode(cls, subject: Union[str, Any], expires_delta : timedelta = expires_delta) -> Token:
        expiration = datetime.utcnow() + expires_delta
        to_encode = { "subject": str(subject), "exp" : expiration }
        encoded_token = jwt.encode(to_encode ,cls.secret, algorithm = cls.algorithm)
        return Token(access_token = encoded_token, token_type = "bearer")

    @classmethod
    def decode(cls, token : Token) -> Dict:
        try:
            decoded_token = jwt.decode(token.access_token, cls.secret, algorithms = [cls.algorithm])
            return decoded_token
        
        except ExpiredSignatureError as expired_error:
            raise ValueError("Token has expired") from expired_error
        
        except JWTError as jwt_error:
            raise ValueError("Invalid token") from jwt_error
        

