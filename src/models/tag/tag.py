from typing import List, TYPE_CHECKING
from src import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


if TYPE_CHECKING:
    from src.models.historic_site.historic_site import HistoricSite


tag_historic_site = db.Table(
    "tag_historic_site",
    db.Column(
        "tag_id",
        db.Integer,
        db.ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "historic_site_id",
        db.Integer,
        db.ForeignKey("historic_sites.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    slug: Mapped[str] = mapped_column(String(40), nullable=False)

    historic_sites: Mapped[List["HistoricSite"]] = relationship(
        secondary=tag_historic_site, back_populates="tags"
    )
