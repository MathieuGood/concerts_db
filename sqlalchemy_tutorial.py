import random
from typing import Any
from sqlalchemy import CursorResult, Engine, create_engine, text


# engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
engine: Engine = create_engine("sqlite+pysqlite:///db_test.sqlite", echo=True)

with engine.connect() as conn:
    result = conn.execute(text("SELECT  'Hello big world!'"))
    print(result.all())
print("")

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS some_table (x INT, y INT)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": random.randint(0, 200), "y": random.randint(0, 200)}],
    )
    conn.commit()
print("")


with engine.connect() as conn:
    result: CursorResult[Any] = conn.execute(text("SELECT * FROM some_table"))
    print(result.all())
print("")



