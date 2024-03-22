from typing import TYPE_CHECKING, List

from sqlalchemy import String
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.declarative_base import Base
from core.models.custom_type import time, email
from src.app.authentication.schemas.user_auth import UserRead

if TYPE_CHECKING:
    from .news_letter import NewsLetter
    from .role import Role
    from src.app.comment.models import Comment


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "User_Table"

    username: Mapped[str]
    time: Mapped[time]  # ondelete="CASCADE" - при удалении пользователя удаляет все что с ним связанно
    email: Mapped[email]
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    # relationship не отображаются в бд
    user_subscription: Mapped["NewsLetter"] = relationship("NewsLetter", back_populates="user", uselist=False)
    user_role: Mapped["Role"] = relationship("Role", back_populates="user")
    comment: Mapped[List["Comment"]] = relationship(back_populates="user_comment")
