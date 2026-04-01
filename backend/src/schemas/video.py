from pydantic import BaseModel, ConfigDict


class VideoBase(BaseModel):
    path: str


class VideoCreate(VideoBase):
    concert_id: int


class VideoResponse(VideoBase):
    id: int
    concert_id: int

    model_config = ConfigDict(from_attributes=True)
