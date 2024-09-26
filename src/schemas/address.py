from pydantic import BaseModel, Field
from typing import List, Optional


class AddressBase(BaseModel):
    city: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int
    city: str
    country: str
    venues: Optional[List["VenueResponse"]] = None
    artists: Optional[List["ArtistResponse"]] = None

    class Config:
        from_attributes = True


from schemas.artist import ArtistResponse
from schemas.venue import VenueResponse
