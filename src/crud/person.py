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
        new_person = Person(firstname=person.firstname, lastname=person.lastname)
        db.add(new_person)
        db.commit()
        db.refresh(new_person)
        return new_person
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Person '{new_person.firstname} {new_person.lastname}' already exists.",
        )


def update(db: Session, person_id: int, person: PersonCreate) -> Person:
    try:
        updated_person: Person = db.query(Person).filter(Person.id == person_id).first()
        if updated_person is None:
            raise HTTPException(
                status_code=404, detail=f"Person with ID {person_id} not found."
            )
        updated_person.firstname = person.firstname
        updated_person.lastname = person.lastname
        db.commit()
        db.refresh(updated_person)
        return updated_person
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Person '{person.firstname} {person.lastname}' already exists.",
        )


def delete(db: Session, person_id: int):
    deleted_person: Person = db.query(Person).filter(Person.id == person_id).first()
    if not deleted_person:
        return {"message": f"Person #{person_id} does not exist."}
    db.delete(deleted_person)
    db.commit()
    return {"message": f"Person #{person_id} '{deleted_person.firstname} {deleted_person.lastname}' deleted."}
