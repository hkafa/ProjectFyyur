"""empty message

Revision ID: dd81fe477ea5
Revises: e935a6e9f4ae
Create Date: 2021-05-02 12:03:13.662557

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dd81fe477ea5'
down_revision = 'e935a6e9f4ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('show', 'start_time')
    op.add_column('show', sa.Column('start_time', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('show', 'start_time1')
    # ### end Alembic commands ###
