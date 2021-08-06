"""first working db schemas

Revision ID: 69acdcd5814b
Revises: 
Create Date: 2021-08-06 14:53:36.850032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69acdcd5814b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('mobile', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('url', sa.String(length=300), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('category', sa.String(length=40), nullable=False),
    sa.Column('unit', sa.String(length=20), nullable=False),
    sa.Column('actual_price', sa.Float(precision=3), nullable=False),
    sa.Column('wholesale_price', sa.Float(precision=3), nullable=False),
    sa.Column('retail_price', sa.Float(precision=3), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('mobile', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('stores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=150), nullable=True),
    sa.Column('contact', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(precision=3), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.Column('sale_type', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=1), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store_product',
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
    sa.PrimaryKeyConstraint('store_id', 'product_id')
    )
    op.create_table('product_orders',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(precision=2), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'order_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_orders')
    op.drop_table('store_product')
    op.drop_table('orders')
    op.drop_table('stores')
    op.drop_table('users')
    op.drop_table('products')
    op.drop_table('customers')
    # ### end Alembic commands ###
