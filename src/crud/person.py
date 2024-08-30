from entities.Person import Person
from fastapi import HTTPException
from schemas.PersonSchema import PersonCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, person_id: int):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(
            status_code=404, detail=f"Person with ID {person_id} not found."
        )
    return person


def get_all(db: Session):
    return db.query(Person).all()


def create(db: Session, person: PersonCreate) -> Person:
    try:
        db_person = Person(firstname=person.firstname, lastname=person.lastname)
        db.add(db_person)
        db.commit()
        db.refresh(db_person)
        return db_person
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Person '{db_person.firstname} {db_person.lastname}' already exists.",
        )


def update(db: Session, person_id: int, person: PersonCreate) -> Person:
    try:
        db_person: Person = db.query(Person).filter(Person.id == person_id).first()
        if db_person is None:
            raise HTTPException(
                status_code=404, detail=f"Person with ID {person_id} not found."
            )
        db_person.firstname = person.firstname
        db_person.lastname = person.lastname
        db.commit()
        db.refresh(db_person)
        return db_person
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Person '{person.firstname} {person.lastname}' already exists.",
        )


def delete(db: Session, person_id: int):
    db_person: Person = db.query(Person).filter(Person.id == person_id).first()
    if not db_person:
        return {"message": f"Person #{person_id} does not exist."}
    db.delete(db_person)
    db.commit()
    return {"message": f"Person #{person_id} '{db_person.firstname} {db_person.lastname}' deleted."}
