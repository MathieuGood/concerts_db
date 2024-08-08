import random
from typing import Any
from sqlalchemy import (
    Engine,
    create_engine,
    MetaData,
)
from entities.User import User


def main():
    # engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    engine: Engine = create_engine(
        "sqlite+pysqlite:///database/concerts_db.sqlite", echo=True
    )
    metadata_obj = MetaData()

    # run_table_queries(engine, metadata_obj)

    sandy = User(name="Sandy", fullname="Sandy Cheeks")
    print(sandy)


if __name__ == "__main__":
    main()
