from dataclasses import dataclass
from typing import List
from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from src.entities.Base import Base


@dataclass
class Concert(Base):

    __tablename__ = "concerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    comments: Mapped[str] = mapped_column(nullable=True)

    show_id: Mapped[int] = mapped_column(ForeignKey("shows.id"), nullable=False)
    show: Mapped["Show"] = relationship("Show", back_populates="concerts")

    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), nullable=False)
    artist: Mapped["Artist"] = relationship("Artist", back_populates="concerts")
    photos: Mapped[List["Photo"]] = relationship("Photo", back_populates="concert")
    videos: Mapped[List["Video"]] = relationship("Video", back_populates="concert")


from src.entities.Artist import Artist
from src.entities.Person import Person
from src.entities.Photo import Photo
from src.entities.Video import Video
from src.entities.Show import Show
