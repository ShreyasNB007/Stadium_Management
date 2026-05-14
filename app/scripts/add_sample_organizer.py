from app import create_app, db
from app.models import User
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_sample_organizer():
    try:
        logger.info("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            # Check if organizer already exists
            existing_organizer = User.query.filter_by(username='event_organizer').first()
            if existing_organizer:
                logger.info("Organizer account already exists.")
                return
            
            # Create organizer account
            organizer = User(
                username='event_organizer',
                email='organizer@example.com',
                role='organizer'
            )
            organizer.set_password('organizer123')
            
            logger.info("Adding organizer to database...")
            db.session.add(organizer)
            db.session.commit()
            
            logger.info("Sample organizer added successfully!")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        add_sample_organizer()
    except Exception as e:
        logger.error(f"Failed to add sample organizer: {str(e)}")
        exit(1) 