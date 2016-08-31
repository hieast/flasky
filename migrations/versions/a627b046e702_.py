"""empty message

Revision ID: a627b046e702
Revises: 344f597bb796
Create Date: 2016-08-31 10:37:48.941706

"""

# revision identifiers, used by Alembic.
revision = 'a627b046e702'
down_revision = '344f597bb796'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    ### end Alembic commands ###
