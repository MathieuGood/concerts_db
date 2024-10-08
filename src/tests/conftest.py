import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from config import Config
from src.database.database import get_db
from src.models.base import Base

print("Loading conftest.py")


@pytest.fixture(scope="session")
def engine() -> Engine:
    print(f"Using database URI: {Config.TEST_DATABASE_URI}")
    return create_engine(
        Config.TEST_DATABASE_URI,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def override_get_db():
    def _override_get_db():
        print("Using test database")
        db = test_db
        try:
            yield db
        finally:
            pass

    return _override_get_db


@pytest.fixture(scope="function")
def test_app(override_get_db):
    print("Applying dependency override")
    app.dependency_overrides[get_db] = override_get_db
    yield app
    print("Clearing dependency override")
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(test_app):
    return TestClient(test_app)
