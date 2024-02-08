from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

from src.auth.settings import Settings
from src.auth.adapters import Accounts 
from src.auth.adapters import SessionFactory
from src.auth.models import Credentials
from src.auth.models import Account
from src.auth.models import User
from src.auth.ports import Security

class Users:

    def __init__(self, settings : Settings, security : Security = None):
        self.session_factory = SessionFactory(settings)
        if security:
            self.accounts.security = security

    async def __aenter__(self):
        self.session = self.session_factory()
        self.accounts = Accounts(session=None)
        await self.session.begin()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()

    async def create(self, credentials : Credentials) -> User:
        account = await self.accounts.create(credentials.model_dump())
        user = User(account = account)
        return user
    
    async def delete(self, user : User):   
        await self.accounts.delete(user.account)


class JWTAuth:
    def __init__(self, prefix : str = "/auth", settings : Settings = None):
        if settings:
            self.settings = settings
            self.users = Users(settings = settings)

        self.router = APIRouter(prefix=prefix) 
        self.router.add_api_route("/register", self.register, methods=["POST"])
        

    def mount(self, api : FastAPI):
        api.include_router(self.router)
    
    async def register(self, form_data: OAuth2PasswordRequestForm = Depends()):
        return {"Hello": "World"}
    
    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        return {"Hello": "World"}