from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ArtistBase(BaseModel):
    name: str
    address_id: int


class ArtistCreate(ArtistBase):
    pass


class ArtistResponse(ArtistBase):
    id: int
    name: str
    address_id: int
    concerts: Optional[List["ConcertResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.concert import ConcertResponse
