from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entities.base import Base


class Photo(Base):
    __tablename__ = "photos"
    __table_args__ = (UniqueConstraint("path", "concert_id", name="_path_concert_uc"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(nullable=False)

    concert_id: Mapped[int] = mapped_column(ForeignKey("concerts.id"))
    concert: Mapped["Concert"] = relationship("Concert", back_populates="photos")


from entities.concert import Concert
