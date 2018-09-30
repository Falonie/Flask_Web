"""add authors

Revision ID: e5c6a8609322
Revises: 1d4b073e1bc1
Create Date: 2018-05-09 13:21:13.715000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5c6a8609322'
down_revision = '1d4b073e1bc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author_id', sa.String(length=100), nullable=False))
    op.create_foreign_key(None, 'post', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'author_id')
    # ### end Alembic commands ###
