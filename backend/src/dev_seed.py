"""
Dev-only seed: if DEV_SEED_CSV_DIR is set and the events table is empty,
import the most recent *.csv from that directory on startup.

Intended use: drop prod CSV exports into a local folder, point DEV_SEED_CSV_DIR
at it in backend/.env. Re-running is a no-op once the DB has data — to re-seed,
delete the SQLite file and restart.
"""
import os
from pathlib import Path

from database.database import SessionLocal
from models.event import Event
from scripts.import_csv import import_csv


def _latest_csv(directory: Path) -> Path | None:
    csvs = list(directory.glob("*.csv"))
    if not csvs:
        return None
    return max(csvs, key=lambda p: p.stat().st_mtime)


def seed_if_requested() -> None:
    dir_str = os.getenv("DEV_SEED_CSV_DIR")
    if not dir_str:
        return

    directory = Path(dir_str)
    if not directory.is_dir():
        print(f"[dev_seed] DEV_SEED_CSV_DIR set but directory not found: {directory}")
        return

    csv_path = _latest_csv(directory)
    if csv_path is None:
        print(f"[dev_seed] No *.csv found in {directory}")
        return

    db = SessionLocal()
    try:
        if db.query(Event).count() > 0:
            print(f"[dev_seed] Events table not empty — skipping seed")
            return
    finally:
        db.close()

    print(f"[dev_seed] Seeding DB from {csv_path} (most recent in {directory})…")
    import_csv(csv_path)
