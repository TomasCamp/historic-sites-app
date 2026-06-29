from src import db
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


if TYPE_CHECKING:
    from src.models.user.role import Role


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    lastname: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship(back_populates="users")
