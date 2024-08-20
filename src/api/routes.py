# routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.crud import get_festivals
from database.database import get_db
from entities.Festival import Festival
from schemas.FestivalSchema import FestivalCreate

router = APIRouter()


@router.get("/")
def read_root():
    return "Hello World"


@router.get("/festivals/")
def read_festivals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = get_festivals(db, skip=skip, limit=limit)
    print(result)
    return result

# Create festival
@router.post("/festivals/")
def create_festival(festival: FestivalCreate, db: Session = Depends(get_db)):
    db_festival = Festival(name=festival.name)
    db.add(db_festival)
    db.commit()
    db.refresh(db_festival)
    return db_festival
