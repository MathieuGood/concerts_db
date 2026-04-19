from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user, get_optional_user
from crud.event import create, delete, get, get_all, update
from database.database import get_db
from models.user import User
from schemas.event import EventCreate, EventResponse, EventListResponse
from schemas.response import ApiResponse

router = APIRouter()


def _strip_private_fields(events: list) -> None:
    """Guests don't see free-text comments or who attended."""
    for e in events:
        e.comments = ""
        e.attendees = []
        for c in e.concerts or []:
            c.comments = ""


@router.get("/event/", response_model=ApiResponse[List[EventListResponse]])
async def get_all_events(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    events = get_all(db)
    if current_user is None:
        db.expunge_all()
        _strip_private_fields(events)
    return ApiResponse(success=True, data=events)


@router.get("/event/{event_id}", response_model=ApiResponse[EventResponse])
async def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    event = get(db, event_id)
    if current_user is None:
        db.expunge_all()
        _strip_private_fields([event])
    return ApiResponse(success=True, data=event)


@router.post("/event/", response_model=ApiResponse[EventResponse])
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApiResponse(success=True, data=create(db, event, current_user.id))


@router.put("/event/{event_id}", response_model=ApiResponse[EventResponse])
async def update_event(
    event_id: int,
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApiResponse(success=True, data=update(db, event_id, event, current_user.id))


@router.delete("/event/{event_id}")
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = delete(db, event_id, current_user.id)
    return ApiResponse(success=True, data=None, message=result["message"])
