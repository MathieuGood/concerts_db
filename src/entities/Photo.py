from dataclasses import dataclass
from typing import List
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities.Base import Base


@dataclass
class Photo(Base):

    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(nullable=False)

    concert_id: Mapped[int] = mapped_column(ForeignKey("concerts.id"))
    concert: Mapped["Concert"] = relationship("Concert", back_populates="photos")


from src.entities.Concert import Concert
