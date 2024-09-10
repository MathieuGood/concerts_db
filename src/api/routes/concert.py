from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.concert import get, get_all, create, update, delete
from database.database import get_db
from schemas.ConcertSchema import ConcertCreate

router = APIRouter()
session = Depends(get_db)

router = APIRouter()


@router.get("/concert/{concert_id}")
def get_concert(concert_id: int, db: Session = session):
    return get(db, concert_id)


@router.get("/concert/")
def get_all_concerts(db: Session = session):
    return get_all(db)


# Create concert
@router.post("/concert/")
def create_concert(concert: ConcertCreate, db: Session = session):
    return create(db, concert)


# Update concert
@router.put("/concert/{concert_id}")
def update_concert(concert_id: int, concert: ConcertCreate, db: Session = session):
    return update(db, concert_id, concert)


# Delete concert
@router.delete("/concert/{concert_id}")
def delete_concert(concert_id: int, db: Session = session):
    return delete(db, concert_id)