"""add pedido table

Revision ID: bfa6d9e8c3a4
Revises: e138229e8566
Create Date: 2026-06-17 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfa6d9e8c3a4'
down_revision = 'e138229e8566'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pedido',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('camisa_id', sa.Integer(), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('total', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pendente'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['camisa_id'], ['camisa.id'], ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('pedido')
