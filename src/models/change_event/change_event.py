from src import db
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, String, func


if TYPE_CHECKING:
    from src.models.user.user import User
    from src.models.historic_site.historic_site import HistoricSite


class ChangeEvent(db.Model):
    __tablename__ = "change_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    action: Mapped[str] = mapped_column(String(15), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="change_events")

    historic_site_id: Mapped[int] = mapped_column(
        ForeignKey("historic_sites.id"), nullable=False
    )
    historic_site: Mapped["HistoricSite"] = relationship(back_populates="change_events")
