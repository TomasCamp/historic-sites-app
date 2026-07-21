from src import db
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from src.models.historic_site.category import Category
    from src.models.historic_site.conservation_status import ConservationStatus
    from src.models.tag.tag import Tag
    from src.models.change_event.change_event import ChangeEvent


class HistoricSite(db.Model):
    __tablename__ = "historic_sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    short_description: Mapped[str] = mapped_column(String(255), nullable=False)
    full_description: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(60), nullable=False)
    province: Mapped[str] = mapped_column(String(60), nullable=False)
    inauguration_year: Mapped[int] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    is_visible: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_delete: Mapped[bool] = mapped_column(default=False)
    cover_image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    cover_image_public_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    category: Mapped[List["Category"]] = relationship(back_populates="historic_sites")

    conservation_status_id: Mapped[int] = mapped_column(
        ForeignKey("conservation_statuses.id"), nullable=False
    )
    conservation_status: Mapped[List["ConservationStatus"]] = relationship(
        back_populates="historic_sites"
    )
    tags: Mapped[List["Tag"]] = relationship(
        secondary="tag_historic_site", back_populates="historic_sites"
    )
    change_events: Mapped[List["ChangeEvent"]] = relationship(
        back_populates="historic_site"
    )
