from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import Config


engine = create_engine(Config.DATABASE_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
