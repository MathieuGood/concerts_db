from pydantic import BaseModel, ConfigDict
from typing import Optional
from schemas.city import CityResponse


class VenueBase(BaseModel):
    name: str
    city_id: int


class VenueCreate(VenueBase):
    pass


class VenueResponse(BaseModel):
    id: int
    name: str
    city_id: int
    city: Optional[CityResponse] = None

    model_config = ConfigDict(from_attributes=True)
