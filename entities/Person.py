from pydantic import BaseModel


class Person(BaseModel):
    firstname: str
    lastname: str
