from src import db
from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, func
from flask_login import UserMixin


if TYPE_CHECKING:
    from src.models.user.role import Role
    from src.models.change_event.change_event import ChangeEvent


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    lastname: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_delete: Mapped[bool] = mapped_column(default=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship(back_populates="users")

    change_events: Mapped[List["ChangeEvent"]] = relationship(back_populates="user")

    def has_permission(self, permission_name: str) -> bool:
        """Devuelve True si el rol del usuario contiene el permiso solicitado o es superuser."""

        return self.is_superuser or permission_name in [
            permission.name for permission in self.role.permissions
        ]

    def is_user(self) -> bool:
        """Devuevle True si el rol del usario es Usuario."""
        return self.role.name == "Usuario"
