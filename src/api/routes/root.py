from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.festival import get, get_all, create, update, delete
from database.database import get_db
from entities.Festival import Festival
from schemas.FestivalSchema import FestivalCreate

router = APIRouter()
session = Depends(get_db)


@router.get("/")
def read_root():
    return "Hello World"
