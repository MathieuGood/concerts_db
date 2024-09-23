from typing import List
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.Base import Base


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    __table_args__ = (UniqueConstraint("city", "country", name="_city_country_uc"),)

    venues: Mapped[List["Venue"]] = relationship("Venue", back_populates="address")
    artists: Mapped[List["Artist"]] = relationship("Artist", back_populates="address")


from entities.Venue import Venue
from entities.Artist import Artist
