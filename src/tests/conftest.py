import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from config import Config
from database.database import get_db
from models.base import Base

# from src.database.database import get_db
# from src.models.base import Base

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
def client():
    print(f"Using database URI: {Config.TEST_DATABASE_URI}")
    engine = create_engine(
        Config.TEST_DATABASE_URI,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
