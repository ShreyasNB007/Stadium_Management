from app import create_app, db
from app.models import Stadium
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_sample_stadiums():
    try:
        logger.info("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            # Create sample stadiums
            stadiums = [
                Stadium(
                    name="Modern Arena",
                    location="123 Main Street, Downtown",
                    capacity=50000,
                    facilities="Premium seating, luxury suites, VIP lounges, multiple food courts, merchandise shops",
                    image_url="stadium1.jpg",
                    price_per_hour=1000.00,
                    contact_info="contact@modernarena.com"
                ),
                Stadium(
                    name="Olympic Stadium",
                    location="456 Sports Avenue, Westside",
                    capacity=80000,
                    facilities="Olympic-size track, swimming pool, training facilities, medical center, press rooms",
                    image_url="stadium2.jpg",
                    price_per_hour=2000.00,
                    contact_info="info@olympicstadium.com"
                ),
                Stadium(
                    name="Community Sports Complex",
                    location="789 Park Road, Eastside",
                    capacity=25000,
                    facilities="Multi-purpose courts, community center, fitness center, children's play area",
                    image_url="stadium3.jpg",
                    price_per_hour=500.00,
                    contact_info="community@sportscomplex.com"
                ),
                Stadium(
                    name="Indoor Sports Arena",
                    location="321 Arena Boulevard, Northside",
                    capacity=15000,
                    facilities="Climate control, retractable seating, locker rooms, training facilities",
                    image_url="stadium4.jpg",
                    price_per_hour=750.00,
                    contact_info="arena@indoorsports.com"
                ),
                Stadium(
                    name="National Football Ground",
                    location="654 Stadium Drive, Southside",
                    capacity=60000,
                    facilities="Professional football pitch, training grounds, media center, corporate boxes",
                    image_url="stadium5.jpg",
                    price_per_hour=1500.00,
                    contact_info="info@nationalfootball.com"
                ),
                Stadium(
                    name="Concert Hall Stadium",
                    location="987 Entertainment Way, Midtown",
                    capacity=40000,
                    facilities="Superior acoustics, VIP boxes, artist facilities, multiple stages",
                    image_url="stadium6.jpg",
                    price_per_hour=1200.00,
                    contact_info="events@concerthall.com"
                )
            ]
            
            logger.info("Adding stadiums to database...")
            db.session.add_all(stadiums)
            db.session.commit()
            
            logger.info("Sample stadiums added successfully!")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == '__main__':
    add_sample_stadiums() 