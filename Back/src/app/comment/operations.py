from .models import Comment
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


class CommentOperations:
    @staticmethod
    async def create_comment(session: AsyncSession, comment_dict: dict) -> int:
        stmt = Comment(**comment_dict)
        session.add(stmt)
        await session.flush()
        await session.commit()
        return stmt.comment_id

    @staticmethod
    async def delete_comment(session: AsyncSession, comment_id: int) -> str:
        stmt = delete(Comment).where(Comment.comment_id == comment_id)
        await session.execute(stmt)
        await session.commit()

        return f"[!] Комментарий {comment_id} успешно удален"

    @staticmethod
    async def redact_comment(session: AsyncSession, comment_id):
        ...
