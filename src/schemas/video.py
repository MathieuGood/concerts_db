from typing import Optional
from pydantic import BaseModel, Field


class VideoBase(BaseModel):
    path: str


class VideoCreate(VideoBase):
    concert_id: int


class VideoResponse(VideoBase):
    id: int
    concert: Optional["ConcertResponse"] = None

    class Config:
        from_attributes = True


from schemas.concert import ConcertResponse