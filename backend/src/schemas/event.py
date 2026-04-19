from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from schemas.venue import VenueResponse
from schemas.festival import FestivalResponse
from schemas.concert import ConcertCreate, ConcertResponse, ConcertListResponse
from schemas.attendee import AttendeeResponse


class EventBase(BaseModel):
    name: Optional[str] = None
    event_date: date
    comments: str


class EventCreate(EventBase):
    venue_id: int
    festival_id: Optional[int] = None
    attendees_ids: Optional[List[int]] = []
    concerts: List[ConcertCreate] = []


class EventResponse(EventBase):
    id: int
    user_id: int
    venue_id: int
    festival_id: Optional[int] = None
    venue: Optional[VenueResponse] = None
    festival: Optional[FestivalResponse] = None
    concerts: Optional[List[ConcertResponse]] = None
    attendees: Optional[List[AttendeeResponse]] = None

    model_config = ConfigDict(from_attributes=True)


class EventListResponse(EventBase):
    """Lightweight event for list — omits artist.country."""
    id: int
    user_id: int
    venue_id: int
    festival_id: Optional[int] = None
    venue: Optional[VenueResponse] = None
    festival: Optional[FestivalResponse] = None
    concerts: Optional[List[ConcertListResponse]] = None
    attendees: Optional[List[AttendeeResponse]] = None

    model_config = ConfigDict(from_attributes=True)
