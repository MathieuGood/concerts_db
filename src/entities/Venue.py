from dataclasses import dataclass
from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities.Base import Base


@dataclass
class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped["Address"] = relationship(back_populates="venues")

    shows : Mapped[List["Show"]] = relationship("Show", back_populates="venue")


from src.entities.Address import Address
from src.entities.Concert import Concert
from src.entities.Show import Show