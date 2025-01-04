from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.dao.utils import set_block_row_if
from src.data.models.general import AccountOrm


async def get_by_id(s: AsyncSession, id_: int, block_row: bool = False) -> AccountOrm | None:
    query = select(AccountOrm).filter(AccountOrm.id == id_)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()

async def get_by_phone_number(s: AsyncSession, phone_number: str, block_row: bool = False) -> AccountOrm | None:
    query = select(AccountOrm).filter(AccountOrm.phone_number == phone_number)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def create(s: AsyncSession, phone_number: str, nickname: str) -> AccountOrm:
    session = AccountOrm(phone_number=phone_number, nickname=nickname)
    s.add(session)
    await s.flush()
    return session


async def delete(s: AsyncSession, account: AccountOrm):
    await s.delete(account)
