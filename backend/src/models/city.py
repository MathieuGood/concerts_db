from typing import List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class City(Base):
    __tablename__ = "cities"
    __table_args__ = (UniqueConstraint("name", "country_id", name="_name_country_uc"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    country: Mapped["Country"] = relationship(back_populates="cities")

    venues: Mapped[List["Venue"]] = relationship("Venue", back_populates="city")


from models.country import Country
from models.venue import Venue
