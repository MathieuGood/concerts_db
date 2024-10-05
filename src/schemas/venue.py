from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class VenueBase(BaseModel):
    name: str


class VenueCreate(VenueBase):
    address_id: int


class VenueResponse(BaseModel):
    id: int
    name: str
    address_id: int
    address: Optional["AddressResponse"] = None
    shows: Optional[List["ShowResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.address import AddressResponse
from schemas.show import ShowResponse
