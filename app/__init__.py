from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from config import Config
import os
from flask_moment import Moment

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # Register custom Jinja2 filters
    @app.template_filter('status_color')
    def status_color(status):
        colors = {
            'pending': 'warning',
            'approved': 'success',
            'rejected': 'danger'
        }
        return colors.get(status, 'secondary')

    # Register blueprints
    from app.routes import main, auth, admin, organizer
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(organizer.bp)

    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Serve uploaded files
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    with app.app_context():
        # Create database tables
        db.create_all()
        
        @app.shell_context_processor
        def make_shell_context():
            return {
                'db': db,
                'User': User,
                'Stadium': Stadium,
                'Event': Event,
                'TimeSlot': TimeSlot,
                'Ticket': Ticket
            }

    return app