"""added unique constrint

Revision ID: 87c60a460d85
Revises: 1257507ee9b5
Create Date: 2021-08-14 15:02:50.340851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87c60a460d85'
down_revision = '1257507ee9b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_check_constraint(
        "ck_orders_status",
        "orders",
        sa.column('status').in_(["PAID", "PENDING", "NOT_PAID", "PARTIAL_PAID", "REFUND"])
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("ck_orders_status")
    # ### end Alembic commands ###

