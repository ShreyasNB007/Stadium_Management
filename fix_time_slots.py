from app import db, create_app
from app.models import TimeSlot, Stadium

def fix_time_slots():
    app = create_app()
    with app.app_context():
        # Get a valid stadium ID
        valid_stadium = Stadium.query.first()
        if not valid_stadium:
            print("No valid stadium found. Cannot fix time slots.")
            return

        # Find problematic time slots
        problematic_slots = TimeSlot.query.filter(
            (TimeSlot.stadium_id.is_(None)) | 
            (~TimeSlot.stadium_id.in_([s.id for s in Stadium.query.all()]))
        ).all()

        if not problematic_slots:
            print("No problematic time slots found.")
            return

        print(f"Found {len(problematic_slots)} problematic time slots.")

        # Update or delete problematic slots
        for slot in problematic_slots:
            slot.stadium_id = valid_stadium.id
            print(f"Updated time slot {slot.id} to stadium {valid_stadium.id}")

        db.session.commit()
        print("Time slots fixed successfully.")

if __name__ == "__main__":
    fix_time_slots() 