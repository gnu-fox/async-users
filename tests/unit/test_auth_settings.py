import pytest
from src.auth.settings import Settings

def test_settings():
    settings = Settings(database_uri = "database")
    
    assert settings.database_uri == "database"