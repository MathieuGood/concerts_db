from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.base import Base


class Concert(Base):
    __tablename__ = "concerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    comments: Mapped[str] = mapped_column(default="", nullable=False)
    setlist: Mapped[str] = mapped_column(nullable=True)

    show_id: Mapped[int] = mapped_column(ForeignKey("shows.id"), nullable=False)
    show: Mapped["Show"] = relationship("Show", back_populates="concerts")

    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), nullable=False)
    artist: Mapped["Artist"] = relationship("Artist", back_populates="concerts")
    photos: Mapped[List["Photo"]] = relationship("Photo", back_populates="concert")
    videos: Mapped[List["Video"]] = relationship("Video", back_populates="concert")


from entities.artist import Artist
from entities.attendee import Attendee
from entities.photo import Photo
from entities.video import Video
from entities.show import Show
