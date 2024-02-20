from uuid import UUID

from pydantic import BaseModel
from pydantic import Field
from datetime import timedelta

from src.auth.models.tokens import Token
from src.auth.models.tokens import Claim
from src.auth.models.tokens import Tokenizer
from src.auth.models.credentials import Credentials

class Account(BaseModel):
    id : UUID = Field(..., alias="id", description="The UUID of the Account")
    authenticated : bool = Field(default=False, alias="authenticated", description="The authentication status of the Account")
    credentials : Credentials = None

    def create_token(self, timedelta : timedelta = timedelta(minutes=15)) -> Token:
        claim = Claim(sub=self.id, exp=timedelta)
        return Tokenizer.encode(claim)
    
    def verify(self, credentials : Credentials) -> bool:
        if credentials.password:
            return self.credentials.verify(credentials.password)