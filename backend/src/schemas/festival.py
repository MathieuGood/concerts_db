from pydantic import BaseModel, ConfigDict
from typing import Optional


class FestivalBase(BaseModel):
    name: str
    year: Optional[int] = None


class FestivalCreate(FestivalBase):
    pass


class FestivalResponse(FestivalBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
