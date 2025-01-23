from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.dao.utils import set_block_row_if
from src.data.models.general import PhraseOrm


async def get_by_id(
        s: AsyncSession,
        id_: int,
        block_row: bool = False
) -> PhraseOrm | None:
    query = select(PhraseOrm).filter(PhraseOrm.id == id_)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def get_by_account_id_and_phrase_lower(
        s: AsyncSession,
        account_id: int,
        phrase_lower: str,
        block_row: bool = False
) -> PhraseOrm | None:
    query = select(PhraseOrm).filter(PhraseOrm.account_id == account_id).filter(PhraseOrm.phrase_lower == phrase_lower)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def get_all_by_account_id(
        s: AsyncSession,
        account_id: int,
        limit: int,
        page: int,
        block_row: bool = False,
) -> tuple[PhraseOrm, ...] | None:
    query = select(PhraseOrm).filter(PhraseOrm.account_id == account_id)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return tuple(r.scalars().all())


async def get_total_count_by_account_id(
        s: AsyncSession,
        account_id: int,
) -> int | None:
    query = select(func.count()).select_from(PhraseOrm).filter(PhraseOrm.account_id == account_id)
    r = await s.execute(query)
    return r.scalar()


async def get_random_one_by_account_id(
        s: AsyncSession,
        account_id: int,
        block_row: bool = False,
) -> PhraseOrm:
    query = select(PhraseOrm).filter(PhraseOrm.account_id == account_id)
    query = query.order_by(func.random()).limit(limit=1)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def create(
        s: AsyncSession,
        account_id: int,
        phrase: str,
        translations: list[str]
) -> PhraseOrm:
    phrase = PhraseOrm(account_id=account_id, phrase=phrase, phrase_lower=phrase.lower(), translations=translations)
    s.add(phrase)
    await s.flush()
    return phrase


async def delete(s: AsyncSession, phrase: PhraseOrm):
    await s.delete(phrase)
