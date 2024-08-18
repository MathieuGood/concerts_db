from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from entities import Base
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
    print("Current diretory :")
    # input("Press Enter to continue...")
    print(os.getcwd())
    print("")


def get_db_session() -> Session:
    engine = create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
        echo=True,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()
