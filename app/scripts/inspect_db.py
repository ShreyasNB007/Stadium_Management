from app import create_app, db
from app.models import User, Stadium, Event, TimeSlot, Booking, Review, Weather, Category
from sqlalchemy import inspect, MetaData
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def inspect_database():
    try:
        logger.info("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            logger.info("Starting database inspection...")
            
            # Get the inspector
            inspector = inspect(db.engine)
            
            # Get all table names from the database
            db_tables = set(inspector.get_table_names())
            logger.info("\nTables found in database:")
            for table in sorted(db_tables):
                logger.info(f"- {table}")
            
            # Get all model tables
            model_tables = set()
            for model in [User, Stadium, Event, TimeSlot, Booking, Review, Weather, Category]:
                model_tables.add(model.__tablename__)
            
            logger.info("\nTables defined in models:")
            for table in sorted(model_tables):
                logger.info(f"- {table}")
            
            # Find tables that exist in database but not in models
            extra_tables = db_tables - model_tables
            if extra_tables:
                logger.info("\nWARNING: Found tables in database that are not defined in models:")
                for table in sorted(extra_tables):
                    logger.info(f"- {table}")
            else:
                logger.info("\nNo extra tables found in database.")
            
            # Find tables that are in models but not in database
            missing_tables = model_tables - db_tables
            if missing_tables:
                logger.info("\nWARNING: Found models that don't have corresponding tables in database:")
                for table in sorted(missing_tables):
                    logger.info(f"- {table}")
            else:
                logger.info("\nNo missing tables found.")
            
            # Check for column mismatches in each table
            logger.info("\nChecking for column mismatches...")
            for model in [User, Stadium, Event, TimeSlot, Booking, Review, Weather, Category]:
                table_name = model.__tablename__
                if table_name in db_tables:
                    logger.info(f"\nInspecting table: {table_name}")
                    
                    # Get columns from database
                    db_columns = {col['name'] for col in inspector.get_columns(table_name)}
                    
                    # Get columns from model
                    model_columns = {c.name for c in model.__table__.columns}
                    
                    # Find extra columns in database
                    extra_columns = db_columns - model_columns
                    if extra_columns:
                        logger.info(f"  Extra columns in database:")
                        for col in sorted(extra_columns):
                            logger.info(f"  - {col}")
                    
                    # Find missing columns in database
                    missing_columns = model_columns - db_columns
                    if missing_columns:
                        logger.info(f"  Missing columns in database:")
                        for col in sorted(missing_columns):
                            logger.info(f"  - {col}")
                    
                    if not extra_columns and not missing_columns:
                        logger.info("  No column mismatches found.")
            
            logger.info("\nDatabase inspection completed!")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == '__main__':
    inspect_database() 