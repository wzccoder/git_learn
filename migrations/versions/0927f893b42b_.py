"""empty message

Revision ID: 0927f893b42b
Revises: 5f97727f7ebc
Create Date: 2020-09-07 17:40:51.319683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0927f893b42b'
down_revision = '5f97727f7ebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answer', 'create_time')
    # ### end Alembic commands ###