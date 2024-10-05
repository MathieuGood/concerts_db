from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.show import get, get_all, create, update, delete
from database.database import get_db
from schemas.show import ShowCreate, ShowResponse

router = APIRouter()
session = Depends(get_db)


@router.get("/show/{show_id}")
async def get_show(show_id: int, db: Session = session):
    return get(db, show_id)


# @router.get("/show/")
# async def get_all_shows(db: Session = session):
#     return get_all(db)


@router.get("/show/", response_model=list[ShowResponse])
async def get_all_shows(db: Session = session):
    return get_all(db)


# Create show
@router.post("/show/")
async def create_show(show: ShowCreate, db: Session = session):
    return create(db, show)


# Update show
@router.put("/show/{show_id}")
async def update_show(show_id: int, show: ShowCreate, db: Session = session):
    return update(db, show_id, show)


# Delete show
@router.delete("/show/{show_id}")
async def delete_show(show_id: int, db: Session = session):
    return delete(db, show_id)
