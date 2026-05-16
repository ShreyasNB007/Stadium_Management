from app import create_app, db
from app.models import User, Stadium, Event, Booking, TimeSlot
from config import Config

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Stadium': Stadium,
        'Event': Event,
        'Booking': Booking,
        'TimeSlot': TimeSlot
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(host='0.0.0.0', port=5000, debug=True)