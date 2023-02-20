"""New Migration

Revision ID: 34eff736d4e0
Revises: d30179ffe864
Create Date: 2023-02-20 03:29:27.734771

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '34eff736d4e0'
down_revision = 'd30179ffe864'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prices',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('unix_time', sa.Integer(), nullable=True),
    sa.Column('date_time_utc', sa.DateTime(timezone=True), nullable=True),
    sa.Column('date_time_gmt_5', sa.DateTime(timezone=True), nullable=True),
    sa.Column('open_price', sa.Float(), nullable=True),
    sa.Column('close_price', sa.Float(), nullable=True),
    sa.Column('low_price', sa.Float(), nullable=True),
    sa.Column('high_price', sa.Float(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.Column('asset_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('indicators',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('unix_time', sa.Integer(), nullable=True),
    sa.Column('price_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['price_id'], ['prices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pricesCrypto',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('qav', sa.Float(), nullable=True),
    sa.Column('num_trades', sa.Integer(), nullable=True),
    sa.Column('taker_base_vol', sa.Float(), nullable=True),
    sa.Column('taker_quote_vol', sa.Float(), nullable=True),
    sa.Column('ignore', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['prices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pricesCrypto')
    op.drop_table('indicators')
    op.drop_table('prices')
    # ### end Alembic commands ###
