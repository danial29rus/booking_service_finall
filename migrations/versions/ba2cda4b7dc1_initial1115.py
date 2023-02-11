"""Initial1115

Revision ID: ba2cda4b7dc1
Revises: adfd11376922
Create Date: 2023-02-08 19:48:37.799556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba2cda4b7dc1'
down_revision = 'adfd11376922'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hotels', 'category_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_foreign_key(None, 'hotels', 'hotels_categories', ['category_id'], ['id'])
    op.alter_column('hotels_categories', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.create_unique_constraint(None, 'hotels_categories', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'hotels_categories', type_='unique')
    op.alter_column('hotels_categories', 'id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.drop_constraint(None, 'hotels', type_='foreignkey')
    op.alter_column('hotels', 'category_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
