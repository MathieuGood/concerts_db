from dataclasses import dataclass
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.Base import Base


@dataclass
class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped["Address"] = relationship(back_populates="venues")

    shows: Mapped[List["Show"]] = relationship("Show", back_populates="venue")


from entities.Address import Address
from entities.Concert import Concert
from entities.Show import Show
