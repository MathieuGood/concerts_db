"""
Add attendees to the database for the admin user.

Usage (on VPS):
    docker exec concerts_db-backend-1 uv run python src/scripts/add_attendees.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.database import SessionLocal
from models.user import User
from models.attendee import Attendee

ATTENDEES = [
    ("Agnès",     "Maillard"),
    ("Franck",    "Ludwig"),
    ("Valentin",  "Novi"),
    ("Tristan",   "Ferry"),
    ("Alexandre", "Degeorges"),
    ("Mathieu",   "Frank"),
]

def main():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.is_admin == True).first()
        if not admin:
            print("ERROR: no admin user found.")
            sys.exit(1)

        for firstname, lastname in ATTENDEES:
            exists = db.query(Attendee).filter(
                Attendee.firstname == firstname,
                Attendee.lastname == lastname,
                Attendee.user_id == admin.id,
            ).first()
            if exists:
                print(f"  skip  {firstname} {lastname} (already exists)")
            else:
                db.add(Attendee(firstname=firstname, lastname=lastname, user_id=admin.id))
                print(f"  added {firstname} {lastname}")

        db.commit()
        print("Done.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
