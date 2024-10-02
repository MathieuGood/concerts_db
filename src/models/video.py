from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Video(Base):
    __tablename__ = "videos"
    __table_args__ = (UniqueConstraint("path", "concert_id", name="_videopath_concert_uc"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(nullable=False)

    concert_id: Mapped[int] = mapped_column(ForeignKey("concerts.id"))
    concert: Mapped["Concert"] = relationship("Concert", back_populates="videos")


from models.concert import Concert
