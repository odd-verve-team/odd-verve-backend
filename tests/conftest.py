import pytest
from rest_framework.test import APIClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from unittest.mock import patch

from config.database import Base
from apps.artworks.models import  Artwork, Category
from apps.users.models import User

# Використовуємо SQLite в пам'яті для швидкого прогону тестів
TEST_DATABASE_URL = "sqlite://"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope="function", autouse=True)
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    TestSessionMaker = scoped_session(
        sessionmaker(
            bind=connection,
            autocommit=False,
            autoflush=False
        )
    )
    
    # Мокаємо SessionLocal у config.database для всіх views
    with patch("config.database.SessionLocal", TestSessionMaker):
        yield TestSessionMaker()

    TestSessionMaker.remove()
    transaction.rollback()
    connection.close()

@pytest.fixture
def api_client():
    return APIClient()