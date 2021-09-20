"""barcode,customer

Revision ID: e4b480014ced
Revises: 87c60a460d85
Create Date: 2021-09-08 15:25:02.624282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4b480014ced'
down_revision = '87c60a460d85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('customers', 'first_name',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    op.create_unique_constraint(op.f('uq_customers_mobile'), 'customers', ['mobile'])
    op.add_column('products', sa.Column('barcode', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'barcode')
    op.drop_constraint(op.f('uq_customers_mobile'), 'customers', type_='unique')
    op.alter_column('customers', 'first_name',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    # ### end Alembic commands ###