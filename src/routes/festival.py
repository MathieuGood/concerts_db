from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.festival import get, get_all, create, update, delete
from database.database import get_db
from schemas.festival import FestivalCreate

router = APIRouter()
session = Depends(get_db)

router = APIRouter()


@router.get("/festival/{festival_id}")
async def get_festival(festival_id: int, db: Session = session):
    return get(db, festival_id)


@router.get("/festival/")
async def get_all_festivals(db: Session = session):
    return get_all(db)


# Create festival
@router.post("/festival/")
async def create_festival(festival: FestivalCreate, db: Session = session):
    return create(db, festival)


# Update festival
@router.put("/festival/{festival_id}")
async def update_festival(festival_id: int, festival: FestivalCreate, db: Session = session):
    return update(db, festival_id, festival)


# Delete festival
@router.delete("/festival/{festival_id}")
async def delete_festival(festival_id: int, db: Session = session):
    return delete(db, festival_id)
