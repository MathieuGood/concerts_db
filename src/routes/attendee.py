from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.attendee import get, get_all, create, update, delete
from database.database import get_db
from schemas.attendee import AttendeeCreate

router = APIRouter()
session = Depends(get_db)


@router.get("/attendee/{attendee_id}")
async def get_attendee(attendee_id: int, db: Session = session):
    return get(db, attendee_id)


@router.get("/attendee/")
async def get_all_attendees(db: Session = session):
    return get_all(db)


# Create attendee
@router.post("/attendee/")
async def create_attendee(attendee: AttendeeCreate, db: Session = session):
    return create(db, attendee)


# Update attendee
@router.put("/attendee/{attendee_id}")
async def update_attendee(
    attendee_id: int, attendee: AttendeeCreate, db: Session = session
):
    return update(db, attendee_id, attendee)


# Delete attendee
@router.delete("/attendee/{attendee_id}")
async def delete_attendee(attendee_id: int, db: Session = session):
    return delete(db, attendee_id)
