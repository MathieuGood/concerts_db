from entities.attendee import Attendee
from fastapi import HTTPException
from schemas.attendee import AttendeeCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, attendee_id: int):
    attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
    if not attendee:
        raise HTTPException(
            status_code=404, detail=f"Attendee with ID {attendee_id} not found."
        )
    return attendee


def get_all(db: Session):
    return db.query(Attendee).all()


def create(db: Session, attendee: AttendeeCreate) -> Attendee:
    try:
        new_attendee = Attendee(firstname=attendee.firstname, lastname=attendee.lastname)
        db.add(new_attendee)
        db.commit()
        db.refresh(new_attendee)
        return new_attendee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Attendee '{new_attendee.firstname} {new_attendee.lastname}' already exists.",
        )


def update(db: Session, attendee_id: int, attendee: AttendeeCreate) -> Attendee:
    try:
        updated_attendee: Attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
        if updated_attendee is None:
            raise HTTPException(
                status_code=404, detail=f"Attendee with ID {attendee_id} not found."
            )
        updated_attendee.firstname = attendee.firstname
        updated_attendee.lastname = attendee.lastname
        db.commit()
        db.refresh(updated_attendee)
        return updated_attendee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Attendee '{attendee.firstname} {attendee.lastname}' already exists.",
        )


def delete(db: Session, attendee_id: int):
    deleted_attendee: Attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
    if not deleted_attendee:
        return {"message": f"Attendee #{attendee_id} does not exist."}

    if deleted_attendee.shows:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete '{deleted_attendee.firstname} {deleted_attendee.lastname}', they are still associated with shows.",
        )
    try:
        db.delete(deleted_attendee)
        db.commit()
        return {
            "message": f"Attendee #{attendee_id} '{deleted_attendee.firstname} {deleted_attendee.lastname}' deleted."
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete '{deleted_attendee.firstname} {deleted_attendee.lastname}' is still referenced in other tables.",
        )
