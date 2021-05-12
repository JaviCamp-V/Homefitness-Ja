"""empty message

Revision ID: 2e96d30f03c4
Revises: c4730d14f909
Create Date: 2021-05-11 18:14:02.943945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e96d30f03c4'
down_revision = 'c4730d14f909'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mets_table',
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('met', sa.Float(), nullable=True),
    sa.Column('heading', sa.String(length=50), nullable=True),
    sa.Column('activities', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mets_table')
    # ### end Alembic commands ###
