"""empty message

Revision ID: 89edc398ee90
Revises: 2031c32c63b7
Create Date: 2017-10-14 10:00:59.134000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89edc398ee90'
down_revision = '2031c32c63b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shoppinglists', 'share_staus')
    op.drop_column('shoppinglists', 'shared_by')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shoppinglists', sa.Column('shared_by', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('shoppinglists', sa.Column('share_staus', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###