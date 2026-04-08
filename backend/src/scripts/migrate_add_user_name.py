"""
Migration: add name column to users table, set name='Mathieu' for the admin user.

Run on the VPS after deploying:
    docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_user_name.py

Safe to run multiple times.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.database import engine
from sqlalchemy import text

ADMIN_EMAIL = "bon.mathieu@gmail.com"
ADMIN_NAME = "Mathieu"


def column_exists(conn, table, column):
    result = conn.execute(text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in result)


def migrate():
    with engine.begin() as conn:
        if not column_exists(conn, "users", "name"):
            conn.execute(text("ALTER TABLE users ADD COLUMN name TEXT"))
            print("Added name column to users table.")
        else:
            print("users.name already exists — skipping ALTER.")

        conn.execute(
            text("UPDATE users SET name = :name WHERE email = :email AND (name IS NULL OR name = '')"),
            {"name": ADMIN_NAME, "email": ADMIN_EMAIL},
        )
        print(f"Set name='{ADMIN_NAME}' for {ADMIN_EMAIL}.")

    print("\nMigration complete.")


if __name__ == "__main__":
    migrate()
