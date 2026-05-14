"""update foreign key constraints

Revision ID: update_foreign_keys
Revises: 
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'update_foreign_keys'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Drop only the actual existing foreign key constraints
    op.drop_constraint('fk_time_slot_stadium', 'time_slot', type_='foreignkey')
    op.drop_constraint('time_slot_ibfk_2', 'time_slot', type_='foreignkey')
    op.drop_constraint('fk_event_stadium', 'event', type_='foreignkey')
    op.drop_constraint('fk_event_organizer', 'event', type_='foreignkey')
    op.drop_constraint('fk_event_time_slot', 'event', type_='foreignkey')
    op.drop_constraint('event_ibfk_4', 'event', type_='foreignkey')
    op.drop_constraint('fk_review_stadium', 'review', type_='foreignkey')
    op.drop_constraint('review_ibfk_2', 'review', type_='foreignkey')
    op.drop_constraint('fk_weather_stadium', 'weather', type_='foreignkey')
    op.drop_constraint('fk_booking_event', 'booking', type_='foreignkey')
    op.drop_constraint('booking_ibfk_1', 'booking', type_='foreignkey')

    # Modify category_id to allow NULL values
    op.alter_column('event', 'category_id',
                    existing_type=sa.Integer(),
                    nullable=True)

    # Recreate constraints with ON DELETE CASCADE or SET NULL
    op.create_foreign_key(
        'fk_time_slot_stadium', 'time_slot',
        'stadium', ['stadium_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_event_stadium', 'event',
        'stadium', ['stadium_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_event_organizer', 'event',
        'user', ['organizer_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_event_time_slot', 'event',
        'time_slot', ['time_slot_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_review_stadium', 'review',
        'stadium', ['stadium_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_weather_stadium', 'weather',
        'stadium', ['stadium_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_booking_event', 'booking',
        'event', ['event_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_event_category', 'event',
        'category', ['category_id'], ['id'],
        ondelete='SET NULL'
    )

def downgrade():
    # Drop the new foreign key constraints
    op.drop_constraint('fk_time_slot_stadium', 'time_slot', type_='foreignkey')
    op.drop_constraint('fk_event_stadium', 'event', type_='foreignkey')
    op.drop_constraint('fk_event_organizer', 'event', type_='foreignkey')
    op.drop_constraint('fk_event_time_slot', 'event', type_='foreignkey')
    op.drop_constraint('fk_review_stadium', 'review', type_='foreignkey')
    op.drop_constraint('fk_weather_stadium', 'weather', type_='foreignkey')
    op.drop_constraint('fk_booking_event', 'booking', type_='foreignkey')
    op.drop_constraint('fk_event_category', 'event', type_='foreignkey')

    # Make category_id NOT NULL again
    op.alter_column('event', 'category_id',
                    existing_type=sa.Integer(),
                    nullable=False)

    # Recreate the original foreign key constraints
    op.create_foreign_key(
        'time_slot_ibfk_1', 'time_slot',
        'stadium', ['stadium_id'], ['id']
    )
    op.create_foreign_key(
        'event_ibfk_1', 'event',
        'stadium', ['stadium_id'], ['id']
    )
    op.create_foreign_key(
        'event_ibfk_2', 'event',
        'user', ['organizer_id'], ['id']
    )
    op.create_foreign_key(
        'event_ibfk_3', 'event',
        'time_slot', ['time_slot_id'], ['id']
    )
    op.create_foreign_key(
        'review_ibfk_1', 'review',
        'stadium', ['stadium_id'], ['id']
    )
    op.create_foreign_key(
        'weather_ibfk_1', 'weather',
        'stadium', ['stadium_id'], ['id']
    )
    op.create_foreign_key(
        'booking_ibfk_2', 'booking',
        'event', ['event_id'], ['id']
    ) 