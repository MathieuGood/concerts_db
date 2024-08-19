from pydantic import BaseModel
from typing import List, Optional


class PersonBase(BaseModel):
    firstname: str
    lastname: Optional[str] = None


class PersonCreate(PersonBase):
    pass


class PersonResponse(PersonBase):
    id: int
    shows: Optional[List["ShowResponse"]] = []

    class Config:
        from_attributes = True


from schemas.ShowSchema import ShowResponse
