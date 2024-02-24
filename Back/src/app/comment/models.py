from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base.declarative_base import Base
from src.base.custom_type import intpk, time

if TYPE_CHECKING:
    from src.app.authentication.models.user import User


class Comment(Base):
    __tablename__ = "Comment_Table"

    comment_id: Mapped[intpk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("User_Table.id"))
    data_comment: Mapped[time]
    comment: Mapped[str]
    user_comment: Mapped["User"] = relationship(back_populates="comment")
