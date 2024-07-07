from datetime import datetime

from pydantic import BaseModel


class Festival(BaseModel):
    name: str
    year: int
    start_date: datetime
    end_date: datetime
