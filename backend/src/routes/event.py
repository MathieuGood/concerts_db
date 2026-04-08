from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from crud.event import get, get_all, create, update, delete
from database.database import get_db
from schemas.event import EventCreate, EventResponse
from schemas.response import ApiResponse
from auth.dependencies import get_current_user
from models.user import User

router = APIRouter()


@router.get("/event/", response_model=ApiResponse[List[EventResponse]])
async def get_all_events(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=get_all(db, current_user.id))


@router.get("/event/{event_id}", response_model=ApiResponse[EventResponse])
async def get_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=get(db, event_id, current_user.id))


@router.post("/event/", response_model=ApiResponse[EventResponse])
async def create_event(event: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=create(db, event, current_user.id))


@router.put("/event/{event_id}", response_model=ApiResponse[EventResponse])
async def update_event(event_id: int, event: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApiResponse(success=True, data=update(db, event_id, event, current_user.id))


@router.delete("/event/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = delete(db, event_id, current_user.id)
    return ApiResponse(success=True, data=None, message=result["message"])
