"""empty message

Revision ID: 9c2a59eed020
Revises: b714b4b5a619
Create Date: 2023-08-09 03:06:06.335945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c2a59eed020'
down_revision = 'b714b4b5a619'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('birth_year', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=64), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('skin_color', sa.String(length=120), nullable=True),
    sa.Column('eye_color', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=120), nullable=True),
    sa.Column('terrain', sa.String(length=120), nullable=True),
    sa.Column('gravity', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###
