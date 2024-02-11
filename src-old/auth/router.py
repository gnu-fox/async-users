from typing import Annotated

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.settings import Settings, DEFAULT_SETTINGS
from src.users.models import Credentials
from src.users.models import SecretStr
from src.users.models import Account
from src.auth.security import JWT, Token
from src.backend.services import UnitOfWork
from src.backend.services import SessionFactory

class Auth:
    def __init__(self, prefix = '/auth', settings : Settings = None):
        self.settings = settings if settings else DEFAULT_SETTINGS
        self.router = APIRouter(prefix = prefix)
        self.router.add_api_route('/login', self.login, methods = ['POST'], response_model=Token)
        self.router.add_api_route('/register', self.register, methods = ['POST'])

        self.uow = UnitOfWork(session_factory=SessionFactory(url=self.settings.database_url))
        self.tokenizer = JWT()

    async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        async with self.uow as uow:
            credentials = Credentials(username=form_data.username, password=SecretStr(form_data.password))
            account = await uow.accounts.read(credentials)
            if not account:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Account not found')

            verified = await uow.accounts.verify(credentials)
            if verified:
                token = self.tokenizer.encode(subject=account.id)
                return token
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong password')

   
    async def register(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        async with self.uow as uow:
            credentials = Credentials(username=form_data.username, password=SecretStr(form_data.password))
            account = await uow.accounts.read(credentials)
            if account:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Account already exists')
            
            account = await uow.accounts.create(credentials)
            await uow.commit()
            token = self.tokenizer.encode(subject=account.id)
            return token


            



    def mount(self, api : FastAPI):
        api.include_router(self.router)