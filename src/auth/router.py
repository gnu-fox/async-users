from typing import Annotated

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.settings import Settings

class Auth:
    def __init__(self, prefix = '/auth', settings : Settings = None):
        self.settings = settings
        self.router = APIRouter(prefix = prefix)
        self.router.add_api_route('/login', self.login, methods = ['POST'])
        self.router.add_api_route('/register', self.register, methods = ['POST'])
    
    async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        return {'Hello': 'World'}
    
    async def register(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        return {'Hello': 'World'}

    def mount(self, api : FastAPI):
        api.include_router(self.router)