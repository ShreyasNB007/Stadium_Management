from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
from flask import url_for

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'organizer', or 'customer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships - only define outgoing relationships here
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Remove the events relationship from here since it's defined in Event model

class Stadium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    facilities = db.Column(db.String(500))
    image_url = db.Column(db.String(200))
    price_per_hour = db.Column(db.Float, nullable=False)
    contact_info = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships with cascade delete
    time_slots = db.relationship('TimeSlot', 
                               backref='stadium', 
                               lazy='dynamic', 
                               cascade='all, delete-orphan',
                               passive_deletes=True)
    reviews = db.relationship('Review', 
                            backref='stadium', 
                            lazy='dynamic', 
                            cascade='all, delete-orphan',
                            passive_deletes=True)
    weather = db.relationship('Weather', 
                            backref='stadium', 
                            lazy='dynamic', 
                            cascade='all, delete-orphan',
                            passive_deletes=True)
    stadium_events = db.relationship('Event', 
                                   lazy='dynamic', 
                                   cascade='all, delete-orphan',
                                   passive_deletes=True)

    @property
    def formatted_image_url(self):
        if self.image_url:
            if self.image_url.startswith(('http://', 'https://')):
                return self.image_url
            return url_for('static', filename=f'uploads/{self.image_url}')
        return url_for('static', filename='uploads/stadium1.jpg')  # Default image

    def can_be_deleted(self):
        """Check if the stadium can be safely deleted"""
        # Check if there are any active events (not cancelled or completed)
        active_events = self.stadium_events.filter(
            Event.status.in_(['pending', 'approved'])
        ).first()
        if active_events:
            return False, "Cannot delete stadium: It has active events. Please cancel or complete these events first."
        return True, None

class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Remove the events relationship since we no longer link events to time slots

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    total_tickets = db.Column(db.Integer, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_date = db.Column(db.Date, nullable=False)  # Date of the event
    event_time = db.Column(db.Time, nullable=False)  # Time of the event
    duration_hours = db.Column(db.Integer, nullable=False, default=2)  # Duration in hours
    thumbnail = db.Column(db.String(256), nullable=True)
    
    # Foreign keys with ondelete CASCADE
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.id', ondelete='CASCADE'), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='SET NULL'))
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id', ondelete='SET NULL'))
    
    # Define relationships with unique backref names
    stadium = db.relationship('Stadium', backref=db.backref('events', lazy='dynamic'))
    organizer = db.relationship('User', backref=db.backref('organized_events', lazy='dynamic'))
    category = db.relationship('Category', backref=db.backref('category_events', lazy='dynamic'))
    time_slot = db.relationship('TimeSlot', backref=db.backref('event', uselist=False))
    bookings = db.relationship('Booking', 
                             backref='event', 
                             lazy='dynamic', 
                             cascade='all, delete-orphan',
                             passive_deletes=True)

    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)
        if 'status' not in kwargs:
            self.status = 'pending'  # Default status for new events
        
        # Create and link time slot if date and time are provided
        if 'event_date' in kwargs and 'event_time' in kwargs and 'duration_hours' in kwargs:
            self._create_time_slot()
    
    def _create_time_slot(self):
        """Create a time slot for this event"""
        from datetime import datetime, timedelta
        
        # Combine date and time
        start_datetime = datetime.combine(self.event_date, self.event_time)
        end_datetime = start_datetime + timedelta(hours=self.duration_hours)
        
        # Create new time slot
        time_slot = TimeSlot(
            stadium_id=self.stadium_id,
            start_time=start_datetime,
            end_time=end_datetime,
            is_available=False  # Mark as unavailable since it's booked
        )
        
        # Add to session but don't commit yet
        db.session.add(time_slot)
        db.session.flush()  # This will generate the time_slot.id
        
        # Link the time slot to this event
        self.time_slot_id = time_slot.id

    def can_be_edited(self):
        """Check if the event can be edited based on its status"""
        return self.status != 'approved'
    
    def can_be_deleted(self):
        """Check if the event can be deleted based on its status"""
        return self.status != 'approved' and not self.bookings
    
    def approve(self):
        """Approve the event"""
        if self.status == 'pending':
            self.status = 'approved'
            return True
        return False
    
    def reject(self):
        """Reject the event"""
        if self.status == 'pending':
            self.status = 'rejected'
            # Make the time slot available again
            if self.time_slot:
                self.time_slot.is_available = True
            return True
        return False
    
    def __repr__(self):
        return f'<Event {self.name}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'confirmed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seat_no = db.Column(db.String(20))
    stand = db.Column(db.String(50))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float)  # in Celsius
    condition = db.Column(db.String(50))  # e.g., 'Sunny', 'Rainy', 'Cloudy'
    humidity = db.Column(db.Integer)  # percentage
    wind_speed = db.Column(db.Float)  # km/h
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 