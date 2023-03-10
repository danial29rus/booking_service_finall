"""Initial127

Revision ID: aad9dc0cbcff
Revises: 67e3c2083d16
Create Date: 2023-02-08 18:58:41.143906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aad9dc0cbcff'
down_revision = '67e3c2083d16'
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
