import pytest
from app.core.database import Base, SessionLocal, get_db

def test_base_metadata_exists():
    assert Base.metadata is not None
    # Just asserting the object is a MetaData instance
    assert type(Base.metadata).__name__ == 'MetaData'

def test_sessionlocal_exists():
    assert SessionLocal is not None
    assert type(SessionLocal).__name__ == 'sessionmaker'

def test_get_db_yields_generator():
    db_gen = get_db()
    assert hasattr(db_gen, '__next__')
