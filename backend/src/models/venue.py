from typing import List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Venue(Base):
    __tablename__ = "venues"
    __table_args__ = (UniqueConstraint("name", "city_id", name="_name_city_uc"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), index=True)
    city: Mapped["City"] = relationship(back_populates="venues")

    events: Mapped[List["Event"]] = relationship("Event", back_populates="venue")


from models.city import City
from models.event import Event
