from pydantic import BaseModel, ConfigDict
from typing import Optional
from schemas.country import CountryResponse


class ArtistBase(BaseModel):
    name: str
    country_id: Optional[int] = None


class ArtistCreate(ArtistBase):
    pass


class ArtistResponse(ArtistBase):
    id: int
    country: Optional[CountryResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ArtistListResponse(BaseModel):
    """Lightweight artist for event list — omits country."""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
