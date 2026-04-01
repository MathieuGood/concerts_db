from pydantic import BaseModel, ConfigDict


class PhotoBase(BaseModel):
    path: str


class PhotoCreate(PhotoBase):
    concert_id: int


class PhotoResponse(PhotoBase):
    id: int
    concert_id: int

    model_config = ConfigDict(from_attributes=True)
