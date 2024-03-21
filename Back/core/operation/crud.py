from typing import TYPE_CHECKING

from sqlalchemy import select

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
