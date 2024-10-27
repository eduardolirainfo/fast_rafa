"""update user

Revision ID: 2c4acc8ac0ba
Revises: 1b50a1d7c011
Create Date: 2024-10-27 12:59:27.605606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c4acc8ac0ba'
down_revision: Union[str, None] = '1b50a1d7c011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'data_nascimento')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('data_nascimento', sa.DATETIME(), nullable=False))
    # ### end Alembic commands ###
