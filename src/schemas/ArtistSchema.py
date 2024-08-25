from pydantic import BaseModel
from typing import List, Optional


class ArtistBase(BaseModel):
    name: str
    country: str


class ArtistCreate(ArtistBase):
    pass


class ArtistResponse(ArtistBase):
    id: int
    name: str
    country: str
    concerts: Optional[List["ConcertResponse"]] = None

    class Config:
        from_attributes = True


from schemas.ConcertSchema import ConcertResponse
