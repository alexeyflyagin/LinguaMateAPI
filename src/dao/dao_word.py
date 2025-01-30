from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.utils import set_block_row_if
from src.data.models.general import WordOrm


async def get_by_id(
        s: AsyncSession,
        id_: int,
        block_row: bool = False
) -> WordOrm | None:
    query = select(WordOrm).filter(WordOrm.id == id_)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def get_by_id_and_account_id(
        s: AsyncSession,
        id_: int,
        account_id: int,
        block_row: bool = False
) -> WordOrm | None:
    query = select(WordOrm).filter(WordOrm.id == id_).filter(WordOrm.account_id == account_id)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def get_by_account_id_and_word(
        s: AsyncSession,
        account_id: int,
        word: str,
        block_row: bool = False
) -> WordOrm | None:
    query = select(WordOrm).filter(WordOrm.account_id == account_id).filter(WordOrm.word == word.lower())
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def get_all_by_account_id(
        s: AsyncSession,
        account_id: int,
        limit: int,
        page: int,
        block_row: bool = False,
) -> tuple[WordOrm, ...] | None:
    query = select(WordOrm).filter(WordOrm.account_id == account_id)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return tuple(r.scalars().all())


async def get_total_count_by_account_id(
        s: AsyncSession,
        account_id: int,
) -> int | None:
    query = select(func.count()).select_from(WordOrm).filter(WordOrm.account_id == account_id)
    r = await s.execute(query)
    return r.scalar()


async def get_random_one_by_account_id(
        s: AsyncSession,
        account_id: int,
        block_row: bool = False,
) -> WordOrm:
    query = select(WordOrm).filter(WordOrm.account_id == account_id)
    query = query.order_by(func.random()).limit(limit=1)
    query = set_block_row_if(query, block_row)
    r = await s.execute(query)
    return r.scalar_one_or_none()


async def create(
        s: AsyncSession,
        account_id: int,
        word: str,
        translations: list[str],
        transcription: str | None = None,
) -> WordOrm:
    word = WordOrm(account_id=account_id, word=word, translations=translations, transcription=transcription)
    s.add(word)
    await s.flush()
    return word


async def delete(s: AsyncSession, word: WordOrm):
    await s.delete(word)
