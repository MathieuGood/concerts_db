from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Concert(Base):
    __tablename__ = "concerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    comments: Mapped[str] = mapped_column(default="", nullable=False)
    setlist: Mapped[str] = mapped_column(nullable=True)
    i_played: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="0")

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)
    event: Mapped["Event"] = relationship("Event", back_populates="concerts")

    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), nullable=False, index=True)
    artist: Mapped["Artist"] = relationship("Artist", back_populates="concerts")

    def __repr__(self) -> str:
        return f"<Concert id={self.id} artist_id={self.artist_id} event_id={self.event_id}>"


from models.artist import Artist
from models.event import Event
