import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from src.entities.Base import Base


def create_session() -> Session:
    try:
        os.remove("database/concerts_db.sqlite")
        print("*** Database file removed ***")
    except FileNotFoundError as e:
        print(e)
        pass

    engine: Engine = create_engine(
        "sqlite+pysqlite:///database/concerts_db.sqlite", echo=True
    )
    # engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    Base.metadata.create_all(engine)
    session = Session(engine)

    return session
