from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class ShowBase(BaseModel):
    name: Optional[str] = None
    event_date: date
    comments: str


class ShowCreate(ShowBase):
    venue_id: int
    festival_id: Optional[int] = None


class ShowResponse(ShowBase):
    id: int
    name: str
    event_date: str
    comments: Optional[str] = None
    venue_id: int
    festival_id: Optional[int] = None
    venue: Optional["VenueResponse"] = None
    concerts: Optional[List["ConcertResponse"]] = None

    class Config:
        from_attributes = True


from schemas.VenueSchema import VenueResponse
from schemas.FestivalSchema import FestivalResponse
from schemas.ConcertSchema import ConcertResponse
from schemas.PersonSchema import PersonResponse
