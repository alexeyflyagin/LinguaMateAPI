import uuid
from datetime import datetime

from sqlalchemy import BIGINT, DateTime, ForeignKey, VARCHAR, JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models.declarative_base import Base

CASCADE = "CASCADE"


class AccountOrm(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    nickname: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    phone_number: Mapped[str] = mapped_column(VARCHAR, nullable=False)


class SessionOrm(Base):
    __tablename__ = "session"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    date_last_activity: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    account_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(column="account.id", ondelete=CASCADE), nullable=False)
    token: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)


class WordOrm(Base):
    __tablename__ = "word"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(name='word_account_id_fkey', column="account.id",
                                                               ondelete=CASCADE), nullable=False)
    word: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    translations: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    transcription: Mapped[str] = mapped_column(VARCHAR, nullable=True)


class PhraseOrm(Base):
    __tablename__ = "phrase"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(column="account.id", ondelete=CASCADE), nullable=False)
    phrase: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    phrase_lower: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    translations: Mapped[list[str]] = mapped_column(JSON, nullable=False)
