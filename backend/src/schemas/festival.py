from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class FestivalBase(BaseModel):
    name: str


class FestivalCreate(FestivalBase):
    pass


class FestivalResponse(FestivalBase):
    id: int
    shows: Optional[List["ShowResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


from schemas.show import ShowResponse
