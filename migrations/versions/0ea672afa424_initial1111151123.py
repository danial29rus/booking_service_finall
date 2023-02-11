"""Initial1111151123

Revision ID: 0ea672afa424
Revises: 5f5029d56274
Create Date: 2023-02-10 21:14:58.872430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ea672afa424'
down_revision = '5f5029d56274'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))
    op.drop_column('users', 'email')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', 'username')
    # ### end Alembic commands ###
