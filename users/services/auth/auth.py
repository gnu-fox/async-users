from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from users.settings import Settings
from users.adapters.repository import Accounts
from users.ports.messagebus import MessageBus

class Auth:
    def __init__(self, settings : Settings, prefix : str = "/auth"):
        self.settings = settings
        self.router = APIRouter(prefix=prefix)
        self.repository = Accounts(settings)
        self.messagebus = MessageBus(self.repository)

    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        ...


    async def register(self, form_data: OAuth2PasswordRequestForm = Depends()):
        ...
    
    def mount(self, api: FastAPI):
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/register", self.register, methods=["POST"])
        api.include_router(self.router)