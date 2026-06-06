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

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Setup test DB tables
    NISBaseModel.metadata.create_all(bind=engine)
    
    # Override get_db in the main FastAPI app
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Teardown test DB
    NISBaseModel.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
