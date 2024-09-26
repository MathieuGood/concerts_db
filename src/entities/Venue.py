from typing import List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.base import Base


class Venue(Base):
    __tablename__ = "venues"
    __table_args__ = (UniqueConstraint("name", "address_id", name="_name_address_uc"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address: Mapped["Address"] = relationship(back_populates="venues")

    shows: Mapped[List["Show"]] = relationship("Show", back_populates="venue")


from entities.address import Address
from entities.concert import Concert
from entities.show import Show
