from dataclasses import dataclass
from typing import List
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities.Base import Base


@dataclass
class Video(Base):

    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String, nullable=False)

    concert_id: Mapped[int] = mapped_column(ForeignKey("concerts.id"))
    concert: Mapped["Concert"] = relationship("Concert", back_populates="videos")


from src.entities.Concert import Concert
