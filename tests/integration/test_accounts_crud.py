import os
import socket
import pytest
import asyncio

from src.users.adapters.unit_of_work import Repositories, URL

@pytest.fixture
def url()->URL:
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_HOST = socket.gethostbyname('postgres')
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')

    return URL.create(
        drivername='postgresql+asyncpg',
        username=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database=DATABASE_NAME
    )

class Settings:
    url : URL

    def __init__(self, url : URL):
        self.url = url

settings = Settings(url = None)

class Base

    async with begin():
        for repository in selfattr
            repository.session = self.session


class Messages:
    pass

class Users(Base):
    accounts : Accounts()
    profiles : Profiles()
    preferences : Preferences()

    messages : Messages()



def test_users(url : URL):
    users = Users(autocommit = False)

    with users:
        account = users.accounts.create(username = 'test', password = 'test')
        profile = users.profiles.create(account.id, first_name = 'test', last_name = 'test')
        preferences = users.preferences.create(account.id, language = 'en', timezone = 'UTC')
        users.commit()
        

    with users:
        user = users.create(username = 'test', password = 'test')
        user.first_name = 'test'
        user.last_name = 'test'
        user.language = 'en'
        user.timezone = 'UTC'
        user.save()








