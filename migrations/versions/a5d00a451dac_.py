"""empty message

Revision ID: a5d00a451dac
Revises: 9c2a59eed020
Create Date: 2023-08-09 15:20:15.611967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5d00a451dac'
down_revision = '9c2a59eed020'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('birth_year',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('birth_year',
               existing_type=sa.String(length=64),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
