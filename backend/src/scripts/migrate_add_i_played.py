"""
Migration: add i_played column to concerts table.

Safe to re-run (skips if column already exists).

Usage (on VPS):
    docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_i_played.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from database.database import engine


def migrate():
    with engine.connect() as conn:
        cols = conn.execute(text("PRAGMA table_info(concerts)")).fetchall()
        col_names = [c[1] for c in cols]

        if "i_played" in col_names:
            print("Column 'i_played' already exists — skipping.")
            return

        conn.execute(text(
            "ALTER TABLE concerts ADD COLUMN i_played BOOLEAN NOT NULL DEFAULT 0"
        ))
        conn.commit()
        print("Added column 'i_played' to concerts table.")


if __name__ == "__main__":
    migrate()
