from dataclasses import dataclass
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities.Base import Base


@dataclass
class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False)
    address: Mapped["Address"] = relationship("Address", back_populates="venues")


from src.entities.Address import Address
