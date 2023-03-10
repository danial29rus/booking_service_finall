"""new database4

Revision ID: 1f705f881564
Revises: b3996b94b18f
Create Date: 2023-02-21 11:48:36.646579

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1f705f881564'
down_revision = 'b3996b94b18f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('price', sa.Integer(), nullable=False))
    op.add_column('bookings', sa.Column('total_cost', sa.Integer(), sa.Computed('(date_to - date_from) * price', ), nullable=True))
    op.add_column('bookings', sa.Column('total_days', sa.Integer(), sa.Computed('date_to - date_from', ), nullable=True))
    op.alter_column('bookings', 'date_from',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('bookings', 'date_to',
               existing_type=sa.DATE(),
               nullable=False)
    op.add_column('hotels', sa.Column('rooms_quantity', sa.Integer(), nullable=False))
    op.add_column('hotels', sa.Column('image_names', sa.JSON(), nullable=False))
    op.drop_column('hotels', 'category_id')
    op.add_column('rooms', sa.Column('description', sa.String(), nullable=True))
    op.add_column('rooms', sa.Column('image_names', sa.JSON(), nullable=False))
    op.alter_column('rooms', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.drop_column('rooms', 'quantity_left')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('quantity_left', sa.INTEGER(), autoincrement=False, nullable=False))
    op.alter_column('rooms', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=False)
    op.drop_column('rooms', 'image_names')
    op.drop_column('rooms', 'description')
    op.add_column('hotels', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('hotels', 'image_names')
    op.drop_column('hotels', 'rooms_quantity')
    op.alter_column('bookings', 'date_to',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('bookings', 'date_from',
               existing_type=sa.DATE(),
               nullable=True)
    op.drop_column('bookings', 'total_days')
    op.drop_column('bookings', 'total_cost')
    op.drop_column('bookings', 'price')
    # ### end Alembic commands ###
