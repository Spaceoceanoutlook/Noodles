"""edited image del Unic

Revision ID: f853b0c77d14
Revises: a60fa8242566
Create Date: 2024-04-26 14:03:03.211706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f853b0c77d14'
down_revision: Union[str, None] = 'a60fa8242566'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('noodles_image_key', 'noodles', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('noodles_image_key', 'noodles', ['image'])
    # ### end Alembic commands ###
