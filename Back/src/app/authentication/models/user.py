from typing import TYPE_CHECKING

from src.models.base import Base
from src.app.authentication.schemas import UserRead
from src.models.custom_type import time, email

from sqlalchemy import String
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.models.role_models import Role
    from src.models.news_letter_models import NewsLetter


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "User_Table"

    # поле с id создается автоматически алембиком последним столбиком, после миграции импортировать файл
    username: Mapped[str] = mapped_column(nullable=False)  # ondelete="CASCADE" - при удалении пользователя удаляет все что с ним связанно
    time: Mapped[time]
    email: Mapped[email]
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_subscription: Mapped["NewsLetter"] = relationship(back_populates="user")
    role: Mapped["Role"] = relationship(back_populates="user")

    async def to_read_model(self) -> UserRead:
        return UserRead(
            id=self.id, email=self.email, username=self.username, time=self.time,
            is_active=self.is_active, is_superuser=self.is_superuser, is_verified=self.is_verified,
            is_subscription=self.is_subscription
        )
