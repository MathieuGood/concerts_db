from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.attendee import get, get_all, create, update, delete
from database.database import get_db
from schemas.attendee import AttendeeCreate

router = APIRouter()


@router.get("/attendee/{attendee_id}")
async def get_attendee(attendee_id: int, db: Session = Depends(get_db)):
    return get(db, attendee_id)


@router.get("/attendee/")
async def get_all_attendees(db: Session = Depends(get_db)):
    return get_all(db)


# Create attendee
@router.post("/attendee/")
async def create_attendee(attendee: AttendeeCreate, db: Session = Depends(get_db)):
    return create(db, attendee)


# Update attendee
@router.put("/attendee/{attendee_id}")
async def update_attendee(
    attendee_id: int, attendee: AttendeeCreate, db: Session = Depends(get_db)
):
    return update(db, attendee_id, attendee)


# Delete attendee
@router.delete("/attendee/{attendee_id}")
async def delete_attendee(attendee_id: int, db: Session = Depends(get_db)):
    return delete(db, attendee_id)
