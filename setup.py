import os
import subprocess
import sys
import shutil
import mysql.connector
from config import Config

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")
        sys.exit(1)

def reset_alembic_version():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()

        # Drop alembic_version table if it exists
        cursor.execute("DROP TABLE IF EXISTS alembic_version")
        print("Dropped alembic_version table if it existed")

        # Close connection
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error resetting alembic version: {err}")
        sys.exit(1)

def setup():
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(os.path.dirname(__file__), 'app', 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    print("Created uploads directory")

    # Initialize database
    print("\nInitializing database...")
    run_command("python init_db.py")

    # Handle migrations directory
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    if os.path.exists(migrations_dir):
        print("\nRemoving existing migrations directory...")
        shutil.rmtree(migrations_dir)
        print("Migrations directory removed")

    # Reset alembic version table
    print("\nResetting alembic version table...")
    reset_alembic_version()

    # Initialize Flask-Migrate
    print("\nInitializing Flask-Migrate...")
    run_command("flask db init")

    # Create initial migration
    print("\nCreating initial migration...")
    run_command('flask db migrate -m "Initial migration"')

    # Apply migration
    print("\nApplying migration...")
    run_command("flask db upgrade")

    print("\nSetup completed successfully!")

if __name__ == "__main__":
    setup() 