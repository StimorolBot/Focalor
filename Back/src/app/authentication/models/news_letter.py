from uuid import UUID
from typing import TYPE_CHECKING

from src.models.base import Base
from src.models.custom_type import intpk

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.app.authentication.models import User


class NewsLetter(Base):
    __tablename__ = "News_Letter_Table"

    id: Mapped[intpk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("User_Table.id"))
    user: Mapped["User"] = relationship(back_populates="is_subscription")
    email: Mapped[str] = mapped_column(unique=True, default=None, server_default="", nullable=True)
    subscription_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default="", server_default="")
    is_subscription: Mapped[bool] = mapped_column(Boolean, default=False, server_default="")
