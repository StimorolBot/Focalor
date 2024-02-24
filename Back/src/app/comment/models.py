from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .custom_type import intpk

if TYPE_CHECKING:
    from .user import User


class Comment(Base):
    __tablename__ = "Comment_Table"

    id: Mapped[intpk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("User_Table.id"), unique=True)
    email: Mapped[str] = mapped_column(unique=True, default=None, server_default="")
    role: Mapped[str] = mapped_column(String(length=5), default="user", server_default="user")
    user: Mapped["User"] = relationship(back_populates="user_role")
