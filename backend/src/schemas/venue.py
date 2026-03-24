from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class VenueBase(BaseModel):
    name: str
    address_id: int


class VenueCreate(VenueBase):
    pass


class VenueResponse(BaseModel):
    id: int
    # name: str
    # address_id: int
    address: Optional["AddressResponse"] = None
    events: Optional[List["EventResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.address import AddressResponse
from schemas.event import EventResponse
