from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.custom_type import intpk

if TYPE_CHECKING:
    from src.models.user_models import User


class Role(Base):
    __tablename__ = "Role_Table"

    id: Mapped[intpk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("User_Table.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="role")
    role: Mapped[str] = mapped_column(String(length=5), default="user", server_default="user")
