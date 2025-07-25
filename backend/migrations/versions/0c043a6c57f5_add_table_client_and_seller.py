"""add table client and seller

Revision ID: 0c043a6c57f5
Revises: b87615fe33d9
Create Date: 2025-07-09 12:04:04.807688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c043a6c57f5'
down_revision: Union[str, None] = 'b87615fe33d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_client',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['tbl_user.user_id'], onupdate='RESTRICT', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('client_id')
    )
    op.create_table('tbl_seller',
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('seller_description', sa.String(length=500), nullable=True),
    sa.Column('seller_bank_account', sa.String(length=7), nullable=False),
    sa.Column('seller_bank_agency', sa.String(length=6), nullable=False),
    sa.Column('seller_bank_name', sa.String(length=100), nullable=False),
    sa.Column('seller_bank_type', sa.Enum('checking', 'savings', name='bank_type'), nullable=False),
    sa.Column('seller_status', sa.Enum('active', 'inactive', name='seller_status'), server_default='inactive', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['tbl_user.user_id'], onupdate='RESTRICT', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('seller_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tbl_seller')
    op.drop_table('tbl_client')
    # ### end Alembic commands ###
