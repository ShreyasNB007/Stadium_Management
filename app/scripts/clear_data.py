from app import create_app, db
from app.models import User, Stadium, Event, TimeSlot, Booking, Review, Weather, Category
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_data():
    try:
        logger.info("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            logger.info("Starting database cleanup...")
            
            # Delete all data in reverse order of dependencies
            logger.info("Deleting bookings...")
            Booking.query.delete()
            
            logger.info("Deleting reviews...")
            Review.query.delete()
            
            logger.info("Deleting weather data...")
            Weather.query.delete()
            
            logger.info("Deleting events...")
            Event.query.delete()
            
            logger.info("Deleting time slots...")
            TimeSlot.query.delete()
            
            logger.info("Deleting stadiums...")
            Stadium.query.delete()
            
            logger.info("Deleting categories...")
            Category.query.delete()
            
            logger.info("Deleting users...")
            User.query.delete()
            
            # Commit the changes
            db.session.commit()
            
            logger.info("Database cleanup completed successfully!")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        db.session.rollback()
        raise

if __name__ == "__main__":
    try:
        clear_data()
    except Exception as e:
        logger.error(f"Failed to clear data: {str(e)}")
        exit(1) 