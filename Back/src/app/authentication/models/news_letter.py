from uuid import UUID
from .base import Base
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User

from .custom_type import intpk


class NewsLetter(Base):
    __tablename__ = "News_Letter_Table"

    id: Mapped[intpk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("User_Table.id"), unique=True)
    email: Mapped[str] = mapped_column(unique=True, default=None, server_default="")
    subscription_date: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP, default=None, server_default=None)
    is_subscription: Mapped[bool] = mapped_column(default=False, server_default=None)
    user: Mapped["User"] = relationship("User", back_populates="user_subscription", uselist=False)
