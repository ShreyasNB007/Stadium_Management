import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY', SECRET_KEY)
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Shrey_007@localhost/stadium_management_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Flask Configuration
    FLASK_APP = 'run.py'
    FLASK_ENV = 'development'
    DEBUG = True  # Set to False in production

    # Create upload folder if it doesn't exist
    @staticmethod
    def init_app(app):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Database Configuration
    DB_USER = 'root'
    DB_PASSWORD = 'Shrey_007'
    DB_HOST = 'localhost'
    DB_NAME = 'stadium_management_db'

    # API Keys
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY') 