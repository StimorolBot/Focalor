from typing import TYPE_CHECKING, Any

from sqlalchemy import select, update, func

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


class Crud:
    @staticmethod
    async def create(session: "AsyncSession", data_dict: dict, table: "DeclarativeAttributeIntercept"):
        stmt = table(**data_dict)
        session.add(stmt)
        await session.commit()

    @staticmethod
    async def read_all(session: "AsyncSession", table: "DeclarativeAttributeIntercept") -> list:
        query = select(table)
        result = await session.execute(query)
        return [item_dict.__dict__ for item in result.all() for item_dict in item]

    @staticmethod
    async def read_one(session: "AsyncSession", table: "DeclarativeAttributeIntercept",
                       table_field: "DeclarativeAttributeIntercept", login: str):
        query = select(table).where(func.lower(table_field) == func.lower(login))
        results = await session.execute(query)
        return results.unique().scalar_one_or_none()

    @staticmethod
    async def update(session: "AsyncSession", table: "DeclarativeAttributeIntercept", update_field, update_where: Any, data: dict):
        stmt = update(table).where(update_field == update_where).values(data)
        await session.execute(stmt)
        await session.commit()
