import random
from typing import Any
from sqlalchemy import (
    CursorResult,
    Engine,
    create_engine,
    text,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase

from entities.User import User


def create_table(engine: Engine) -> None:
    with engine.begin() as conn:
        # conn.execute(text("DELETE FROM some_table"))
        conn.execute(text("CREATE TABLE IF NOT EXISTS some_table (x INT, y INT)"))
    print("")


def delete_table_content(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM some_table"))
    print("")


def insert_entries(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": random.randint(0, 200), "y": random.randint(0, 200)}],
        )
    print("")


def print_results(engine: Engine) -> None:
    with engine.connect() as conn:
        result: CursorResult[Any] = conn.execute(
            text("SELECT * FROM some_table WHERE x < :max_number"), {"max_number": 100}
        )

        for row in result:
            print(f"x is {row.x} and y is {row.y}")

    print("")


def create_user_table(metadata_obj: MetaData) -> Table:
    return Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )


def create_address_table(metadata_obj: MetaData) -> Table:
    return Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_address", String, nullable=False),
    )



def main():
    # engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    engine: Engine = create_engine("sqlite+pysqlite:///database/concerts_db.sqlite", echo=True)
    metadata_obj = MetaData()

    # print_results(engine)

    # user_table = create_user_table(metadata_obj)
    # address_table = create_address_table(metadata_obj)
    # metadata_obj.create_all(engine)

    sandy = User(name="Sandy", fullname="Sandy Cheeks")


if __name__ == "__main__":
    main()
