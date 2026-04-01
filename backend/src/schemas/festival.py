from pydantic import BaseModel, ConfigDict


class FestivalBase(BaseModel):
    name: str


class FestivalCreate(FestivalBase):
    pass


class FestivalResponse(FestivalBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
