"""Initial1111

Revision ID: 67147b1c5b03
Revises: 0a6bc4b8bb84
Create Date: 2023-02-08 19:37:04.254083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67147b1c5b03'
down_revision = '0a6bc4b8bb84'
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
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hotels_categories', 'id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.drop_constraint(None, 'hotels', type_='foreignkey')
    op.alter_column('hotels', 'category_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
