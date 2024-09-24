from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.person import get, get_all, create, update, delete
from database.database import get_db
from schemas.PersonSchema import PersonCreate

router = APIRouter()
session = Depends(get_db)

router = APIRouter()


@router.get("/person/{person_id}")
def get_person(person_id: int, db: Session = session):
    return get(db, person_id)


@router.get("/person/")
def get_all_persons(db: Session = session):
    return get_all(db)


# Create person
@router.post("/person/")
def create_person(person: PersonCreate, db: Session = session):
    return create(db, person)


# Update person
@router.put("/person/{person_id}")
def update_person(person_id: int, person: PersonCreate, db: Session = session):
    return update(db, person_id, person)


# Delete person
@router.delete("/person/{person_id}")
def delete_person(person_id: int, db: Session = session):
    return delete(db, person_id)
