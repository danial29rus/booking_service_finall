"""Initial122

Revision ID: 4506c0bbca27
Revises: 70010c44903d
Create Date: 2023-02-08 18:47:41.000222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4506c0bbca27'
down_revision = '70010c44903d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('category_id', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hotels', 'category_id')
    # ### end Alembic commands ###
