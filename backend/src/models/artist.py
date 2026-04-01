from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Artist(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    country_id: Mapped[Optional[int]] = mapped_column(ForeignKey("countries.id"), nullable=True)
    country: Mapped[Optional["Country"]] = relationship(back_populates="artists")

    concerts: Mapped[List["Concert"]] = relationship("Concert", back_populates="artist")


from models.concert import Concert
from models.country import Country
