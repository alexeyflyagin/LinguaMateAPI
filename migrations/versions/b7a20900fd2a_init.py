"""init

Revision ID: b7a20900fd2a
Revises: 
Create Date: 2025-01-04 22:11:20.621062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7a20900fd2a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('date_create', sa.DateTime(), nullable=False),
    sa.Column('nickname', sa.VARCHAR(), nullable=False),
    sa.Column('phone_number', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('word',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('word', sa.VARCHAR(), nullable=False),
    sa.Column('translates', sa.JSON(), nullable=False),
    sa.Column('transcription', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('account_and_word',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('date_create', sa.DateTime(), nullable=False),
    sa.Column('account_id', sa.BIGINT(), nullable=False),
    sa.Column('word_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['word_id'], ['word.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phrase',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('account_id', sa.BIGINT(), nullable=False),
    sa.Column('phrase', sa.VARCHAR(), nullable=False),
    sa.Column('translates', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('session',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('date_create', sa.DateTime(), nullable=False),
    sa.Column('date_last_activity', sa.DateTime(), nullable=False),
    sa.Column('account_id', sa.BIGINT(), nullable=False),
    sa.Column('token', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session')
    op.drop_table('phrase')
    op.drop_table('account_and_word')
    op.drop_table('word')
    op.drop_table('account')
    # ### end Alembic commands ###