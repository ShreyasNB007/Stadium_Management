from app import create_app, db
from app.models import User, Stadium, Event, TimeSlot
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_data():
    try:
        logger.info("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            logger.info("Starting database operations...")
            
            # Check if data already exists
            if Stadium.query.first() is not None:
                logger.info("Sample data already exists. Skipping creation.")
                return
            
            logger.info("Creating sample stadiums...")
            # Create sample stadiums
            stadiums = [
                Stadium(
                    name="Grand Arena",
                    location="123 Sports Avenue, City Center",
                    capacity=50000,
                    description="A state-of-the-art stadium with modern facilities and excellent viewing angles. Features include premium seating, luxury suites, and world-class amenities.",
                    image_url="uploads/stadium1.jpg"
                ),
                Stadium(
                    name="Olympic Stadium",
                    location="456 Olympic Drive, Sports District",
                    capacity=75000,
                    description="The largest stadium in the region, host to major international events. Known for its iconic architecture and cutting-edge technology.",
                    image_url="uploads/stadium2.jpg"
                ),
                Stadium(
                    name="Community Sports Center",
                    location="789 Local Street, Downtown",
                    capacity=25000,
                    description="A versatile venue perfect for community events and local sports. Features a retractable roof and multi-purpose facilities.",
                    image_url="uploads/stadium3.jpg"
                )
            ]

            logger.info("Creating sample organizer...")
            # Create sample organizer
            organizer = User(
                username="event_organizer",
                email="organizer@example.com",
                password_hash=generate_password_hash("organizer123"),
                role="organizer"
            )

            logger.info("Adding stadiums and organizer to database...")
            # Add all to database
            db.session.add_all(stadiums)
            db.session.add(organizer)
            db.session.commit()

            logger.info("Creating sample events...")
            # Create sample events
            events = []
            for i, event_data in enumerate([
                {
                    "title": "Summer Music Festival",
                    "description": "A three-day music festival featuring top artists from around the world. Experience live performances, food vendors, and interactive art installations.",
                    "start_time": datetime.now() + timedelta(days=30),
                    "end_time": datetime.now() + timedelta(days=32),
                    "stadium_id": stadiums[0].id,
                    "organizer_id": organizer.id,
                    "total_tickets": 45000,
                    "ticket_price": 150.00,
                    "category": "Music",
                    "status": "approved"
                },
                {
                    "title": "International Football Match",
                    "description": "A friendly match between national teams. Watch world-class athletes compete in this exciting international showdown.",
                    "start_time": datetime.now() + timedelta(days=15),
                    "end_time": datetime.now() + timedelta(days=15, hours=3),
                    "stadium_id": stadiums[1].id,
                    "organizer_id": organizer.id,
                    "total_tickets": 70000,
                    "ticket_price": 75.00,
                    "category": "Sports",
                    "status": "approved"
                }
            ]):
                # Create time slot
                time_slot = TimeSlot(
                    start_time=event_data["start_time"],
                    end_time=event_data["end_time"],
                    stadium_id=event_data["stadium_id"]
                )
                db.session.add(time_slot)
                db.session.flush()
                
                # Create event
                event = Event(
                    title=event_data["title"],
                    description=event_data["description"],
                    stadium_id=event_data["stadium_id"],
                    organizer_id=event_data["organizer_id"],
                    total_tickets=event_data["total_tickets"],
                    available_tickets=event_data["total_tickets"],
                    ticket_price=event_data["ticket_price"],
                    category=event_data["category"],
                    status=event_data["status"],
                    time_slot_id=time_slot.id
                )
                time_slot.is_available = False
                events.append(event)
                db.session.add(event)

            logger.info("Adding events to database...")
            db.session.add_all(events)
            db.session.commit()

            logger.info("Creating uploads directory...")
            # Create uploads directory
            uploads_dir = os.path.join(app.static_folder, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            logger.info("Creating placeholder images...")
            # Create placeholder images
            for i in range(1, 4):
                image_path = os.path.join(uploads_dir, f'stadium{i}.jpg')
                if not os.path.exists(image_path):
                    with open(image_path, 'w') as f:
                        f.write('Placeholder image')
            
            logger.info("Sample data creation completed successfully!")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        create_sample_data()
    except Exception as e:
        logger.error(f"Failed to create sample data: {str(e)}")
        sys.exit(1) 