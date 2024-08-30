from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.Base import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(nullable=False)

    concert_id: Mapped[int] = mapped_column(ForeignKey("concerts.id"))
    concert: Mapped["Concert"] = relationship("Concert", back_populates="videos")


from entities.Concert import Concert
