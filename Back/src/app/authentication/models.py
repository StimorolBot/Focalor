from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, TIMESTAMP, String, Integer
from datetime import datetime


class Base(DeclarativeBase):
    ...


class Role(Base):
    __tablename__ = "Role_Table"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(nullable=False)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "User_Table"

    # поле с id создается автоматически алембиком последним столбиком, после миграции импортировать файл
    username: Mapped[str] = mapped_column(default=None, nullable=True)
    user_role: Mapped[int] = mapped_column(Integer, ForeignKey(Role.id))
    time: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
