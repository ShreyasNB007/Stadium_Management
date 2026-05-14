from app import create_app, db
from app.models import Event, TimeSlot, Stadium, User
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_events():
    try:
        logger.info("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            # Get all events
            events = Event.query.all()
            
            if not events:
                logger.info("No events found in the database.")
                return
            
            logger.info(f"Found {len(events)} events:")
            now = datetime.now()
            for event in events:
                # Get related information
                stadium = Stadium.query.get(event.stadium_id)
                organizer = User.query.get(event.organizer_id)
                time_slot = TimeSlot.query.get(event.time_slot_id)
                
                logger.info(f"""
Event ID: {event.id}
Title: {event.title}
Status: {event.status}
Category: {event.category}
Time Slot ID: {event.time_slot_id}
Start Time: {event.start_time.strftime('%Y-%m-%d %H:%M:%S') if event.start_time else 'Not set'} ({event.start_time > now and 'Future' or 'Past' if event.start_time else 'N/A'})
End Time: {event.end_time.strftime('%Y-%m-%d %H:%M:%S') if event.end_time else 'Not set'}
Stadium: {stadium.name if stadium else 'Not found'}
Organizer: {organizer.username if organizer else 'Not found'}
Total Tickets: {event.total_tickets}
Available Tickets: {event.available_tickets}
Ticket Price: ${event.ticket_price:.2f}
Created At: {event.created_at.strftime('%Y-%m-%d %H:%M:%S')}
Time Slot Available: {time_slot.is_available if time_slot else 'No time slot'}
""")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        check_events()
    except Exception as e:
        logger.error(f"Failed to check events: {str(e)}")
        exit(1) 