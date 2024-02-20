from typing import Annotated
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth import exceptions
from src.auth.services import Settings
from src.auth.services import Authentication
from src.auth.adapters.adapters import UnitOfWork, SessionFactory
from src.auth.models.tokens import Token

class Auth:
    def __init__(self, settings : Settings, prefix : str = "/auth"):
        self.uow = UnitOfWork(session_factory=SessionFactory(url=settings.database_uri))
        self.service = Authentication(uow=self.uow)
        self.bearer = OAuth2PasswordBearer(tokenUrl=settings.token_url)
        self.router = APIRouter(prefix=prefix)
        self.router.add_api_route("/login", self.login, methods=["POST"], response_model=Token)
        self.router.add_api_route("/register", self.register, methods=["POST"])
        
    def mount(self, api : FastAPI):
        api.include_router(self.router)

    async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
        try:
            account = await self.service.authenticate(username=form_data.username, password=form_data.password)
            return account.create_token()

        except exceptions.AccountNotFound:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Account not found")
        
        except exceptions.InvalidCredentials:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid credentials")
        
        except Exception as error:
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = str(error))


    async def register(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        try:
            await self.service.register(username=form_data.username, password=form_data.password)
        
        except exceptions.AccountAlreadyExists:
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