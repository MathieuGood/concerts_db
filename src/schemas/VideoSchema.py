from typing import Optional
from pydantic import BaseModel


class VideoBase(BaseModel):
    path: str


class VideoCreate(VideoBase):
    concert_id: int


class VideoResponse(VideoBase):
    id: int
    concert: Optional["ConcertResponse"] = None

    class Config:
        from_attributes = True


from schemas.ConcertSchema import ConcertResponse
