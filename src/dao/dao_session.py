from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.dao.utils import set_block_row_if
from src.data.models.general import SessionOrm


async def get_by_id(s: AsyncSession, id_: str, block_row: bool = False) -> SessionOrm | None:
    query = select(SessionOrm).filter(SessionOrm.id == id_)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def get_by_token(s: AsyncSession, token: UUID, block_row: bool = False) -> SessionOrm | None:
    query = select(SessionOrm).filter(SessionOrm.token == token)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def create(s: AsyncSession, account_id: int, token: UUID) -> SessionOrm:
    session = SessionOrm(account_id=account_id, token=token)
    s.add(session)
    await s.flush()
    return session


async def delete(s: AsyncSession, session: SessionOrm):
    await s.delete(session)
