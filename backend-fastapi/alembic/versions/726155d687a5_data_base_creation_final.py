"""Data Base Creation final

Revision ID: 726155d687a5
Revises: 92873e46232e
Create Date: 2023-03-06 02:46:05.067716

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '726155d687a5'
down_revision = '92873e46232e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pricesCrypto')
    op.add_column('prices', sa.Column('qav', sa.Float(), nullable=True))
    op.add_column('prices', sa.Column('num_trades', sa.Integer(), nullable=True))
    op.add_column('prices', sa.Column('taker_base_vol', sa.Float(), nullable=True))
    op.add_column('prices', sa.Column('taker_quote_vol', sa.Float(), nullable=True))
    op.add_column('prices', sa.Column('ignore', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('prices', 'ignore')
    op.drop_column('prices', 'taker_quote_vol')
    op.drop_column('prices', 'taker_base_vol')
    op.drop_column('prices', 'num_trades')
    op.drop_column('prices', 'qav')
    op.create_table('pricesCrypto',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('qav', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('num_trades', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('taker_base_vol', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('taker_quote_vol', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('ignore', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id'], ['prices.id'], name='pricesCrypto_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='pricesCrypto_pkey')
    )
    # ### end Alembic commands ###
