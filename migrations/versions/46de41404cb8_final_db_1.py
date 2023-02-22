"""Final_db_1

Revision ID: 46de41404cb8
Revises: 0ea672afa424
Create Date: 2023-02-11 20:54:49.967518

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '46de41404cb8'
down_revision = '0ea672afa424'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hotels_categories')
    op.drop_table('bookings')
    op.drop_table('hotels')
    op.drop_table('rooms')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('rooms',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('rooms_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('hotel_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('services', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity_left', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], name='rooms_hotel_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='rooms_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('hotels',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('hotels_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('services', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['hotels_categories.id'], name='hotels_category_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='hotels_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('bookings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('room_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date_from', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('date_to', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], name='bookings_room_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='bookings_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='bookings_pkey')
    )
    op.create_table('hotels_categories',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='hotels_categories_pkey')
    )
    # ### end Alembic commands ###