"""empty message

Revision ID: 03694e944386
Revises: 2e96d30f03c4
Create Date: 2021-05-15 12:01:00.456479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03694e944386'
down_revision = '2e96d30f03c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mets_table', sa.Column('intensity', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mets_table', 'intensity')
    # ### end Alembic commands ###
