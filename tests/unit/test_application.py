import pytest
from uuid import uuid4, UUID
from dataclasses import dataclass

from src.users.models import User, Event, Command
from src.users.models import Account
from src.users.repository import Repository
from src.users.application import Application, Factory
from src.users.services import Handler