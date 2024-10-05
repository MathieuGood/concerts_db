from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


from schemas.artist import ArtistResponse
from schemas.venue import VenueResponse
