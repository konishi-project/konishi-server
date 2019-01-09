"""empty message

Revision ID: 300a4c20df91
Revises: d6651a0d7994
Create Date: 2018-12-10 13:08:05.897416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '300a4c20df91'
down_revision = 'd6651a0d7994'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('public_id', sa.String(length=50), nullable=True))
    op.create_unique_constraint(None, 'user', ['public_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'public_id')
    # ### end Alembic commands ###