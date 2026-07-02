from typing import List, TYPE_CHECKING
from src import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


if TYPE_CHECKING:
    from src.models.user.permission import Permission
    from src.models.user.user import User


role_permission = db.Table(
    "role_permission",
    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Role(db.Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")
    permissions: Mapped[List["Permission"]] = relationship(
        secondary=role_permission, back_populates="roles"
    )
