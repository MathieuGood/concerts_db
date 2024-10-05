from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date


class ShowBase(BaseModel):
    name: Optional[str] = None
    event_date: date
    comments: str


class ShowCreate(ShowBase):
    venue_id: int
    festival_id: Optional[int] = None
    attendees_ids: Optional[List[int]] = None
    concerts: List["ConcertCreate"] = None


class ShowResponse(ShowBase):
    id: int
    name: str
    event_date: str
    comments: Optional[str] = None
    venue_id: int
    festival_id: Optional[int] = None
    venue: Optional["VenueResponse"] = None
    concerts: Optional[List["ConcertResponse"]] = None
    attendees: Optional[List["AttendeeResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.venue import VenueResponse
from schemas.festival import FestivalResponse
from schemas.concert import ConcertResponse
from schemas.concert import ConcertCreate
from schemas.attendee import AttendeeResponse
