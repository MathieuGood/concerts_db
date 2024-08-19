from typing import Optional
from pydantic import BaseModel, Field


class PhotoBase(BaseModel):
    path: str


class PhotoCreate(PhotoBase):
    concert_id: int


class PhotoResponse(PhotoBase):
    id: int
    concert: Optional["ConcertResponse"] = Field(None, exclude=True)

    class Config:
        from_attributes = True


from schemas.ConcertSchema import ConcertResponse
