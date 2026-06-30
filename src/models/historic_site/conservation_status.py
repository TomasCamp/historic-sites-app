from src import db
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from src.models.historic_site.historic_site import HistoricSite


class ConservationStatus(db.Model):
    __tablename__ = "conservation_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15))

    historic_sites: Mapped[List["HistoricSite"]] = relationship(
        back_populates="conservation_status"
    )
