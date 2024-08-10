from dataclasses import dataclass
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.Base import Base


@dataclass
class Address(Base):

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)

    venue: Mapped["Venue"] = relationship("Venue", back_populates="address")


from entities.Venue import Venue
