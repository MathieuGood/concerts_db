from pydantic import BaseModel, Field
from typing import List, Optional


class VenueBase(BaseModel):
    name: str


class VenueCreate(VenueBase):
    address_id: int


class VenueResponse(BaseModel):
    id: int
    name: str
    address_id: int
    address: Optional["AddressResponse"] = Field(None, exclude=True)
    shows: Optional[List["ShowResponse"]] = Field(None, exclude=True)

    class Config:
        from_attributes = True


from schemas.AddressSchema import AddressResponse
from schemas.ShowSchema import ShowResponse
