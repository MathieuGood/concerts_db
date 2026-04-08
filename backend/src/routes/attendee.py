from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.attendee import get, get_all, create, update, delete
from database.database import get_db
from schemas.attendee import AttendeeCreate, AttendeeResponse
from schemas.response import ApiResponse
from auth.dependencies import get_current_user
from models.user import User

router = APIRouter()


@router.get("/attendee/", response_model=ApiResponse[List[AttendeeResponse]])
async def get_all_attendees(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=get_all(db, current_user.id))


@router.get("/attendee/{attendee_id}", response_model=ApiResponse[AttendeeResponse])
async def get_attendee(attendee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=get(db, attendee_id, current_user.id))


@router.post("/attendee/", response_model=ApiResponse[AttendeeResponse])
async def create_attendee(attendee: AttendeeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=create(db, attendee, current_user.id))


@router.put("/attendee/{attendee_id}", response_model=ApiResponse[AttendeeResponse])
async def update_attendee(
    attendee_id: int, attendee: AttendeeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return ApiResponse(success=True, data=update(db, attendee_id, attendee, current_user.id))


@router.delete("/attendee/{attendee_id}")
async def delete_attendee(attendee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = delete(db, attendee_id, current_user.id)
    return ApiResponse(success=True, data=None, message=result["message"])
