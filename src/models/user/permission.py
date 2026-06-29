from src import db
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


if TYPE_CHECKING:
    from src.models.user.role import Role


class Permission(db.Model):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)

    roles: Mapped[List["Role"]] = relationship(
        secondary="role_permission", back_populates="permissions"
    )
