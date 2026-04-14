"""
Migration: add year column to festivals table + change unique constraint.

Also auto-parses trailing 4-digit year from existing festival names:
    "Rock en Seine 2023" -> name="Rock en Seine", year=2023

Safe to re-run (skips if column already exists).

Usage (on VPS):
    docker exec concerts_db-backend-1 uv run python src/scripts/migrate_add_festival_year.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from database.database import engine


YEAR_SUFFIX_RE = re.compile(r"^(.*?)\s+(\d{4})$")


def migrate():
    with engine.connect() as conn:
        cols = conn.execute(text("PRAGMA table_info(festivals)")).fetchall()
        col_names = [c[1] for c in cols]

        if "year" in col_names:
            print("Column 'year' already exists — skipping schema migration.")
        else:
            # SQLite does not support dropping constraints, so we recreate the table.
            print("Recreating festivals table with year column and new unique constraint...")
            conn.execute(text("""
                CREATE TABLE festivals_new (
                    id    INTEGER PRIMARY KEY,
                    name  VARCHAR NOT NULL,
                    year  INTEGER,
                    UNIQUE (name, year)
                )
            """))
            conn.execute(text("""
                INSERT INTO festivals_new (id, name, year)
                SELECT id, name, NULL FROM festivals
            """))
            conn.execute(text("DROP TABLE festivals"))
            conn.execute(text("ALTER TABLE festivals_new RENAME TO festivals"))
            conn.commit()
            print("Schema migration complete.")

        # Auto-parse year from names like "Rock en Seine 2023"
        festivals = conn.execute(text("SELECT id, name, year FROM festivals")).fetchall()
        updated = 0
        for fid, name, year in festivals:
            if year is not None:
                continue  # already has a year, skip
            m = YEAR_SUFFIX_RE.match(name)
            if m:
                new_name = m.group(1).strip()
                new_year = int(m.group(2))
                # Check for name+year collision before updating
                existing = conn.execute(
                    text("SELECT id FROM festivals WHERE name = :n AND year = :y"),
                    {"n": new_name, "y": new_year}
                ).first()
                if existing and existing[0] != fid:
                    print(f"SKIP  id={fid} '{name}' — '{new_name}' ({new_year}) already exists")
                    continue
                conn.execute(
                    text("UPDATE festivals SET name = :n, year = :y WHERE id = :id"),
                    {"n": new_name, "y": new_year, "id": fid}
                )
                print(f"PARSE id={fid} '{name}' -> name='{new_name}', year={new_year}")
                updated += 1

        conn.commit()
        print(f"\nAuto-parsed {updated} festival name(s).")


if __name__ == "__main__":
    migrate()
