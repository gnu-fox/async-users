from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

from src.auth.settings import Settings

class JWTAuth:
    def __init__(self, prefix : str = "/auth", settings : Settings = None):
        self.settings = settings
        self.router = APIRouter(prefix=prefix) 
        self.router.add_api_route("/register", self.register, methods=["POST"])

    def mount(self, api : FastAPI):
        api.include_router(self.router)
    
    async def register(self, form_data: OAuth2PasswordRequestForm = Depends()):
        return {"Hello": "World"}
    
    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        return {"Hello": "World"}