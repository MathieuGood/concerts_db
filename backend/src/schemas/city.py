from pydantic import BaseModel, ConfigDict
from schemas.country import CountryResponse


class CityBase(BaseModel):
    name: str
    country_id: int


class CityCreate(CityBase):
    pass


class CityResponse(BaseModel):
    id: int
    name: str
    country_id: int
    country: CountryResponse

    model_config = ConfigDict(from_attributes=True)
