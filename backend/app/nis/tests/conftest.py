import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_db
from app.nis.models.base import NISBaseModel

from sqlalchemy.pool import StaticPool

# Create an in-memory SQLite engine for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def db():
    # Setup test DB tables for each test to ensure isolation
    NISBaseModel.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    NISBaseModel.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    # Override get_db in the main FastAPI app with the test session
    def override_get_db_for_test():
        yield db

    app.dependency_overrides[get_db] = override_get_db_for_test
    yield TestClient(app)
    app.dependency_overrides.clear()
