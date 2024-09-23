from pydantic import BaseModel
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
    attendees: Optional[List["PersonResponse"]] = None


from schemas.VenueSchema import VenueResponse
from schemas.FestivalSchema import FestivalResponse
from schemas.ConcertSchema import ConcertResponse
from schemas.ConcertSchema import ConcertCreate
from schemas.PersonSchema import PersonResponse
