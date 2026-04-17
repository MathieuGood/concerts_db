from typing import Optional
from models.attendee import Attendee
from fastapi import HTTPException
from schemas.attendee import AttendeeCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get(db: Session, attendee_id: int, user_id: Optional[int] = None):
    q = db.query(Attendee).filter(Attendee.id == attendee_id)
    if user_id is not None:
        q = q.filter(Attendee.user_id == user_id)
    attendee = q.first()
    if not attendee:
        raise HTTPException(
            status_code=404, detail=f"Attendee with ID {attendee_id} not found."
        )
    return attendee


def get_all(db: Session, user_id: Optional[int] = None):
    q = db.query(Attendee)
    if user_id is not None:
        q = q.filter(Attendee.user_id == user_id)
    return q.all()


def create(db: Session, attendee: AttendeeCreate, user_id: int) -> Attendee:
    try:
        new_attendee = Attendee(
            firstname=attendee.firstname, lastname=attendee.lastname, user_id=user_id
        )
        db.add(new_attendee)
        db.commit()
        db.refresh(new_attendee)
        return new_attendee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Attendee '{attendee.firstname} {attendee.lastname}' already exists.",
        )


def update(db: Session, attendee_id: int, attendee: AttendeeCreate, user_id: int) -> Attendee:
    try:
        updated_attendee: Attendee = (
            db.query(Attendee).filter(Attendee.id == attendee_id, Attendee.user_id == user_id).first()
        )
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


def delete(db: Session, attendee_id: int, user_id: int) -> dict[str, str] | HTTPException:
    deleted_attendee: Attendee = (
        db.query(Attendee).filter(Attendee.id == attendee_id, Attendee.user_id == user_id).first()
    )
    if not deleted_attendee:
        return {"message": f"Attendee #{attendee_id} does not exist."}

    if deleted_attendee.events:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete '{deleted_attendee.firstname} {deleted_attendee.lastname}', it is still associated with events.",
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
