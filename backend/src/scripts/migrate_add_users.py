"""
Migration: add users table, add user_id to events and attendees, assign all existing data to admin.

Run ONCE on the VPS after deploying the auth update:
    docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_users.py

Safe to run multiple times (skips if already migrated).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.database import engine
from sqlalchemy import text, inspect

ADMIN_EMAIL = "bon.mathieu@gmail.com"
ADMIN_PASSWORD = "changeme"  # change immediately via admin panel after first login


def column_exists(conn, table, column):
    result = conn.execute(text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in result)


def table_exists(conn, table):
    result = conn.execute(text(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=:t"
    ), {"t": table})
    return result.fetchone() is not None


def migrate():
    from auth.password import hash_password

    with engine.begin() as conn:
        # 1. Create users table if not exists
        if not table_exists(conn, "users"):
            conn.execute(text("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    hashed_password TEXT NOT NULL,
                    is_admin INTEGER NOT NULL DEFAULT 0,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("Created users table.")
        else:
            print("users table already exists — skipping creation.")

        # 2. Insert admin user if not exists
        existing = conn.execute(text("SELECT id FROM users WHERE email = :e"), {"e": ADMIN_EMAIL}).fetchone()
        if not existing:
            hashed = hash_password(ADMIN_PASSWORD)
            conn.execute(text(
                "INSERT INTO users (email, hashed_password, is_admin, created_at) VALUES (:e, :h, 1, CURRENT_TIMESTAMP)"
            ), {"e": ADMIN_EMAIL, "h": hashed})
            print(f"Created admin user: {ADMIN_EMAIL}")
        else:
            print(f"Admin user {ADMIN_EMAIL} already exists.")

        admin_id = conn.execute(text("SELECT id FROM users WHERE email = :e"), {"e": ADMIN_EMAIL}).fetchone()[0]

        # 3. Add user_id to events if not exists
        if not column_exists(conn, "events", "user_id"):
            conn.execute(text("ALTER TABLE events ADD COLUMN user_id INTEGER REFERENCES users(id)"))
            conn.execute(text("UPDATE events SET user_id = :uid WHERE user_id IS NULL"), {"uid": admin_id})
            print(f"Added user_id to events, assigned all to admin (id={admin_id}).")
        else:
            print("events.user_id already exists — skipping.")

        # 4. Rebuild attendees table with user_id (SQLite can't ALTER UNIQUE constraints)
        if not column_exists(conn, "attendees", "user_id"):
            # Create new table with updated schema
            conn.execute(text("""
                CREATE TABLE attendees_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firstname TEXT NOT NULL,
                    lastname TEXT,
                    user_id INTEGER REFERENCES users(id),
                    UNIQUE (firstname, lastname, user_id)
                )
            """))
            conn.execute(text(f"""
                INSERT INTO attendees_new (id, firstname, lastname, user_id)
                SELECT id, firstname, lastname, {admin_id} FROM attendees
            """))
            conn.execute(text("DROP TABLE attendees"))
            conn.execute(text("ALTER TABLE attendees_new RENAME TO attendees"))
            print(f"Rebuilt attendees table with user_id, assigned all to admin (id={admin_id}).")
        else:
            print("attendees.user_id already exists — skipping.")

    print("\nMigration complete.")
    print(f"\n⚠️  Default admin password is '{ADMIN_PASSWORD}' — change it via the admin panel!")


if __name__ == "__main__":
    migrate()
