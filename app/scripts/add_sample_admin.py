from app import create_app, db
from app.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_sample_admin():
    try:
        app = create_app()
        with app.app_context():
            # Check if admin already exists
            admin = User.query.filter_by(username='admin').first()
            if admin:
                logger.info("Admin account already exists")
                return

            # Create admin user
            admin = User(
                username='admin',
                email='admin@stadium.com',
                role='admin'
            )
            admin.set_password('admin123')  # Default password
            
            # Add to database
            db.session.add(admin)
            db.session.commit()
            
            logger.info("Sample admin account created successfully!")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == '__main__':
    add_sample_admin() 