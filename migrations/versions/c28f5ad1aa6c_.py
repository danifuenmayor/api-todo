"""empty message

Revision ID: c28f5ad1aa6c
Revises: 
Create Date: 2020-04-03 15:23:49.507669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c28f5ad1aa6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=150), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    op.drop_table('users')
    # ### end Alembic commands ###