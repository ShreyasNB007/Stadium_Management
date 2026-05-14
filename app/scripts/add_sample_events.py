import os
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Event, Stadium, User, TimeSlot, Category
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_sample_events():
    try:
        logger.info("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            # Get required data
            stadiums = Stadium.query.all()
            organizer = User.query.filter_by(role='organizer').first()
            sports_category = Category.query.filter_by(name='Sports').first()
            
            if not stadiums or not organizer or not sports_category:
                logger.error("Required data not found. Please ensure stadiums, organizer, and sports category exist.")
                return
            
            # Base date for events
            base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Sample events data
            events_data = [
                {
                    'name': 'Summer Music Festival',
                    'description': 'A three-day music festival featuring top artists from around the world.',
                    'event_date': base_date + timedelta(days=30),  # 30 days from now
                    'event_time': datetime.strptime('18:00', '%H:%M').time(),
                    'duration_hours': 4,
                    'stadium_id': stadiums[0].id,
                    'organizer_id': organizer.id,
                    'total_tickets': 40000,
                    'available_tickets': 40000,
                    'category_id': sports_category.id,
                    'thumbnail': 'event1.jpg',
                    'status': 'approved'
                },
                {
                    'name': 'International Football Match',
                    'description': 'Watch the national teams compete in this exciting international match.',
                    'event_date': base_date + timedelta(days=15),  # 15 days from now
                    'event_time': datetime.strptime('20:00', '%H:%M').time(),
                    'duration_hours': 3,
                    'stadium_id': stadiums[1].id,
                    'organizer_id': organizer.id,
                    'total_tickets': 60000,
                    'available_tickets': 60000,
                    'category_id': sports_category.id,
                    'thumbnail': 'event2.jpg',
                    'status': 'approved'
                },
                {
                    'name': 'Local Basketball Tournament',
                    'description': 'Support your local teams in this exciting basketball tournament.',
                    'event_date': base_date + timedelta(days=7),  # 7 days from now
                    'event_time': datetime.strptime('19:00', '%H:%M').time(),
                    'duration_hours': 3,
                    'stadium_id': stadiums[2].id,
                    'organizer_id': organizer.id,
                    'total_tickets': 20000,
                    'available_tickets': 20000,
                    'category_id': sports_category.id,
                    'thumbnail': 'event3.jpg',
                    'status': 'approved'
                }
            ]

            # Add events to database
            for event_data in events_data:
                # Create event
                event = Event(**event_data)
                db.session.add(event)

            try:
                db.session.commit()
                logger.info("Sample events added successfully!")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error adding events: {str(e)}")
                raise
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == '__main__':
    add_sample_events() 