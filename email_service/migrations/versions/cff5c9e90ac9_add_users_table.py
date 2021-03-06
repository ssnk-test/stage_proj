"""add users table

Revision ID: cff5c9e90ac9
Revises: 
Create Date: 2020-08-10 08:22:43.237545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cff5c9e90ac9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('templates',
    sa.Column('name', sa.Unicode(), nullable=True),
    sa.Column('body', sa.Unicode(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('templates')
    # ### end Alembic commands ###
