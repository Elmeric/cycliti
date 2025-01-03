"""Add user table

Revision ID: 4383d2991afc
Revises: 
Create Date: 2024-10-21 17:51:13.872338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4383d2991afc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('birthdate', sa.String(length=10), nullable=False),
    sa.Column('preferred_language', sa.String(length=10), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=False),
    sa.Column('access_type', sa.Integer(), nullable=False),
    sa.Column('photo_path', sa.String(length=254), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
