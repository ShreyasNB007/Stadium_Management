"""merge heads

Revision ID: 018d8c71599d
Revises: 54b588e0044c, update_foreign_keys
Create Date: 2025-05-21 19:39:55.326041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '018d8c71599d'
down_revision = ('54b588e0044c', 'update_foreign_keys')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
