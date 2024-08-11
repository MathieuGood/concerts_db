from dataclasses import dataclass
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities.Base import Base


@dataclass
class Address(Base):

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)

    venues: Mapped[List["Venue"]] = relationship("Venue", back_populates="address")


from src.entities.Venue import Venue
