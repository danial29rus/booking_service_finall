"""Initial124

Revision ID: 31bbedbf6ebb
Revises: 31082751ffb7
Create Date: 2023-02-08 18:55:28.267868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31bbedbf6ebb'
down_revision = '31082751ffb7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'hotels_categories', 'hotels', ['id'], ['category_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'hotels_categories', type_='foreignkey')
    # ### end Alembic commands ###
