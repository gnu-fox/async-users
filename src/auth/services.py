from uuid import uuid4
from uuid import UUID
from typing import Annotated
from typing import Any
from typing import Union

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.models import Token, Claim, Tokenizer
from src.auth.models import Account
from src.auth.models import Credentials
from src.auth.models import BaseSettings
from src.auth.adapters import Accounts
from src.auth.adapters import URL, UnitOfWork, SessionFactory
from src.auth.exceptions import (
    AccountNotFound,
    AccountAlreadyExists,
    WrongPassword
)

class Settings(BaseSettings):
    database_url : Union[str, URL]    

class Users(UnitOfWork):
    def __init__(self, settings : Settings):
        super().__init__(session_factory=SessionFactory(url=settings.database_url))

    async def begin(self):
        await super().begin()
        self.accounts = Accounts(session=self.session)

    async def authenticate(self, **kwargs) -> Account:
        account = await self.accounts.read(credentials=Credentials(**kwargs))
        if not account:
            raise AccountNotFound
        if not account.authenticated:
            raise WrongPassword
        return account
    
    async def register(self, **kwargs):
        account = await self.accounts.read(credentials=Credentials(username=kwargs['username']))
        if account:
            raise AccountAlreadyExists
        
        account = Account(id=uuid4())
        await self.accounts.create(account=account, credentials=Credentials(**kwargs))


class Auth:
    def __init__(self, settings : Settings, prefix : str = "/auth"):
        self.settings = settings
        self.users = Users(settings=settings)
        self.router = APIRouter(prefix=prefix)
        self.bearer = OAuth2PasswordBearer(tokenUrl="token")
        self.router.add_api_route("/login", self.login, methods=["POST"], response_model=Token)
        self.router.add_api_route("/register", self.register, methods=["POST"])

    def mount(self, api : FastAPI):
        api.include_router(self.router)

    async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
        async with self.users as users:
            try:
                account = await users.authenticate(username=form_data.username, password=form_data.password)
                token = account.create_token()
                return token

            except AccountNotFound:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "Account not found")
            
            except WrongPassword:
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail = "Invalid credentials")
            
            except Exception as error:
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = str(error))


    async def register(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        async with self.users as users:
            try:
                await users.register(username=form_data.username, password=form_data.password)
                await users.commit()
            
            except AccountAlreadyExists:
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT, 
                    detail = "Account already exists")
            
            except KeyError:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Invalid credentials")
            
            except Exception as error:
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail = str(error))