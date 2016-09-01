"""empty message

Revision ID: 7d5e2ff01953
Revises: b08fe4835d04
Create Date: 2016-09-01 21:54:02.767893

"""

# revision identifiers, used by Alembic.
revision = '7d5e2ff01953'
down_revision = 'b08fe4835d04'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    ### end Alembic commands ###
