from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.event import get, get_all, create, update, delete
from database.database import get_db
from schemas.event import EventCreate, EventResponse

router = APIRouter()


@router.get("/event/{event_id}")
async def get_event(event_id: int, db: Session = Depends(get_db)):
    return get(db, event_id)


@router.get("/event/")
async def get_all_events(db: Session = Depends(get_db)):
    return get_all(db)


@router.post("/event/")
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    return create(db, event)


@router.put("/event/{event_id}")
async def update_event(event_id: int, event: EventCreate, db: Session = Depends(get_db)):
    return update(db, event_id, event)


@router.delete("/event/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    return delete(db, event_id)
