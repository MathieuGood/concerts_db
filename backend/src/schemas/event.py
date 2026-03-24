from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class EventBase(BaseModel):
    name: Optional[str] = None
    event_date: date
    comments: str


class EventCreate(EventBase):
    venue_id: int
    festival_id: Optional[int] = None
    attendees_ids: Optional[list[int]] = None
    concerts: list["ConcertCreate"] = None


class EventResponse(EventBase):
    id: int
    venue_id: int
    festival_id: Optional[int] = None
    venue: Optional["VenueResponse"] = None
    concerts: Optional[list["ConcertResponse"]] = None
    attendees: Optional[list["AttendeeResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.venue import VenueResponse
from schemas.festival import FestivalResponse
from schemas.concert import ConcertResponse, ConcertCreate
from schemas.attendee import AttendeeResponse
