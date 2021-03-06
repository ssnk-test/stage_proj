"""empty message

Revision ID: ac7ed87bb168
Revises: c0c82d601cd1
Create Date: 2020-08-19 22:41:04.071229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac7ed87bb168'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_table',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('uuid')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.UniqueConstraint('email', name='user_email_key'),
    sa.UniqueConstraint('username', name='user_username_key')
    )
    op.drop_table('users_table')
    # ### end Alembic commands ###
