"""Added Bot table

Revision ID: ddfa2c854b13
Revises: 
Create Date: 2024-09-03 23:26:49.525944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddfa2c854b13'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bot',
    sa.Column('bot_id', sa.BigInteger(), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('thread_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('bot_id'),
    sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_bot_bot_id'), 'bot', ['bot_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bot_bot_id'), table_name='bot')
    op.drop_table('bot')
    # ### end Alembic commands ###
