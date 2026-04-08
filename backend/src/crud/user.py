from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from schemas.user import UserCreate
from auth.password import hash_password, verify_password


def get_all(db: Session):
    return db.query(User).order_by(User.created_at).all()


def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create(db: Session, user_in: UserCreate) -> User:
    if get_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail=f"Email '{user_in.email}' already registered.")
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        name=user_in.name,
        is_admin=user_in.is_admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User:
    user = get_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user


def change_password(db: Session, user: User, current_password: str, new_password: str) -> User:
    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user


def reset_password(db: Session, user_id: int, new_password: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User #{user_id} not found.")
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User #{user_id} not found.")
    db.delete(user)
    db.commit()
    return {"message": f"User #{user_id} '{user.email}' deleted."}
