"""empty message

Revision ID: 398b6b851fd8
Revises: 99b69293f171
Create Date: 2021-04-26 12:50:15.907757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '398b6b851fd8'
down_revision = '99b69293f171'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('seeking_talent_desc', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_talent_desc')
    # ### end Alembic commands ###
