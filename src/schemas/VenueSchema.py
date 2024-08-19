from pydantic import BaseModel
from typing import List, Optional
from schemas.AddressSchema import AddressResponse
from schemas.ShowSchema import ShowResponse


class VenueBase(BaseModel):
    name: str


class VenueCreate(VenueBase):
    address_id: int


class VenueResponse(BaseModel):
    id: int
    name: str
    address_id: int
    address: Optional[AddressResponse] = None
    shows: Optional[List["ShowResponse"]] = None

    class Config:
        from_attributes = True
