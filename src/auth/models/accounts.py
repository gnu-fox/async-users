from uuid import UUID

from pydantic import Field
from datetime import timedelta
from pydantic.dataclasses import dataclass

from src.auth.models.tokens import Token
from src.auth.models.tokens import Claim
from src.auth.models.tokens import Tokenizer
from src.auth.models.credentials import Credential

@dataclass
class Account:
    id : UUID = Field(..., alias="id", description="The UUID of the Account")
    authenticated : bool = Field(default=False, alias="authenticated", description="The authentication status of the Account")
    credential : Credential = None

    def create_token(self, timedelta : timedelta = timedelta(minutes=15)) -> Token:
        claim = Claim(sub=self.id, exp=timedelta)
        return Tokenizer.encode(claim)
    
    def verify(self, credential : Credential) -> bool:
        if credential.password:
            return self.credential.verify(credential.password)