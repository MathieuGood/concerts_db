from pydantic import BaseModel, ConfigDict


class AddressBase(BaseModel):
    city: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
