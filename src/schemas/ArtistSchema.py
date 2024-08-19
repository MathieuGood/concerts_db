from pydantic import BaseModel, Field
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
    concerts: Optional[List["ConcertResponse"]] = Field(None, exclude=True)

    class Config:
        from_attributes = True


from schemas.ConcertSchema import ConcertResponse
