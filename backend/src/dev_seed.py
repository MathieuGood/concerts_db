"""
Dev-only seed: if DEV_SEED_CSV is set and the events table is empty,
import the CSV on startup.

Intended use: drop a CSV (e.g. exported from prod) next to the repo and point
DEV_SEED_CSV at it in backend/.env. Re-running is a no-op once the DB has data —
to re-seed, delete the SQLite file and restart.
"""
import os
from pathlib import Path

from database.database import SessionLocal
from models.event import Event
from scripts.import_csv import import_csv


def seed_if_requested() -> None:
    csv_path_str = os.getenv("DEV_SEED_CSV")
    if not csv_path_str:
        return

    csv_path = Path(csv_path_str)
    if not csv_path.exists():
        print(f"[dev_seed] DEV_SEED_CSV set but file not found: {csv_path}")
        return

    db = SessionLocal()
    try:
        if db.query(Event).count() > 0:
            print(f"[dev_seed] Events table not empty — skipping seed from {csv_path}")
            return
    finally:
        db.close()

    print(f"[dev_seed] Seeding DB from {csv_path}…")
    import_csv(csv_path)
