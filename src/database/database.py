from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from entities.Base import Base
from config import Config


def delete_database() -> None:
    import os

    try:
        os.remove("flask_concerts_db.sqlite")
        print("*** Database file removed ***")
    except FileNotFoundError as e:
        print(e)
        pass

    print("")
    # input("Press Enter to continue...")
    print("Current diretory :")
    print(os.getcwd())
    print("")


def get_db():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



