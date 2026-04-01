from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    cities: Mapped[List["City"]] = relationship("City", back_populates="country")
    artists: Mapped[List["Artist"]] = relationship("Artist", back_populates="country")


from models.city import City
from models.artist import Artist
