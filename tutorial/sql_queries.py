
import random
from typing import Any
from sqlalchemy import CursorResult, Engine, text


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