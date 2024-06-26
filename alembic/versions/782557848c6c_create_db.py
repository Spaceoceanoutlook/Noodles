"""create db

Revision ID: 782557848c6c
Revises: 
Create Date: 2024-04-24 12:25:15.171810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '782557848c6c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_of_country', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name_of_country')
    )
    op.create_table('Noodles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_of_noodles', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('recommendation', sa.Boolean(), nullable=False),
    sa.Column('image', sa.String(length=150), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['Country.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('image'),
    sa.UniqueConstraint('name_of_noodles')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Noodles')
    op.drop_table('Country')
    # ### end Alembic commands ###
