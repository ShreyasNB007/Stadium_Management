"""add stadium_id to time_slot table

Revision ID: fe6eff0d0822
Revises: 7c86e25802a6
Create Date: 2024-03-19 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fe6eff0d0822'
down_revision = '7c86e25802a6'
branch_labels = None
depends_on = None


def upgrade():
    # Do NOT add the column, just update existing rows and add constraints
    conn = op.get_bind()
    # Get the first stadium ID
    result = conn.execute(sa.text("SELECT id FROM stadium LIMIT 1")).fetchone()
    if result:
        stadium_id = result[0]
        # Update all existing time slots to use this stadium
        conn.execute(sa.text(f"UPDATE time_slot SET stadium_id = {stadium_id} WHERE stadium_id IS NULL"))
    # Now make the column non-nullable and add the foreign key
    with op.batch_alter_table('time_slot', schema=None) as batch_op:
        batch_op.alter_column('stadium_id', existing_type=sa.Integer(), nullable=False)
        batch_op.create_foreign_key(None, 'stadium', ['stadium_id'], ['id'])


def downgrade():
    with op.batch_alter_table('time_slot', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        # Do NOT drop the column, as it may be used elsewhere
