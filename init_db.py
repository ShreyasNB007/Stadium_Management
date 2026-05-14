from app import create_app, db
from app.models import User, Stadium, Event, TimeSlot, Category, Booking, Review, Weather
from datetime import datetime, timedelta
import random

def init_db():
    app = create_app()
    with app.app_context():
        # Create admin user
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample organizer
        organizer = User(username='organizer', email='organizer@example.com', role='organizer')
        organizer.set_password('organizer123')
        db.session.add(organizer)
        
        # Create sample customer
        customer = User(username='customer', email='customer@example.com', role='customer')
        customer.set_password('customer123')
        db.session.add(customer)
        
        # Create categories
        categories = [
            Category(name='Sports'),
            Category(name='Music'),
            Category(name='Conference'),
            Category(name='Exhibition'),
            Category(name='Theater')
        ]
        for category in categories:
            db.session.add(category)
        
        # Create sample stadiums
        stadiums = [
            Stadium(
                name='Grand Sports Arena',
                location='123 Sports Lane, City Center',
                capacity=50000,
                description='A state-of-the-art sports facility with modern amenities.',
                image_url='https://example.com/stadium1.jpg',
                price_per_hour=1000.00,
                contact_info='contact@grandsports.com',
                latitude=40.7128,
                longitude=-74.0060
            ),
            Stadium(
                name='Music Hall',
                location='456 Concert Street, Downtown',
                capacity=20000,
                description='Perfect venue for concerts and musical performances.',
                image_url='https://example.com/stadium2.jpg',
                price_per_hour=800.00,
                contact_info='info@musichall.com',
                latitude=40.7589,
                longitude=-73.9851
            ),
            Stadium(
                name='Conference Center',
                location='789 Business Avenue, Tech Park',
                capacity=10000,
                description='Modern conference facility with advanced technology.',
                image_url='https://example.com/stadium3.jpg',
                price_per_hour=600.00,
                contact_info='events@conferencecenter.com',
                latitude=40.7505,
                longitude=-73.9934
            ),
            Stadium(
                name='Exhibition Grounds',
                location='321 Fair Road, Industrial Zone',
                capacity=30000,
                description='Spacious venue for exhibitions and fairs.',
                image_url='https://example.com/stadium4.jpg',
                price_per_hour=500.00,
                contact_info='book@exhibitiongrounds.com',
                latitude=40.7421,
                longitude=-73.9911
            ),
            Stadium(
                name='Theater Complex',
                location='654 Arts Boulevard, Cultural District',
                capacity=5000,
                description='Elegant theater for performances and shows.',
                image_url='https://example.com/stadium5.jpg',
                price_per_hour=400.00,
                contact_info='tickets@theatercomplex.com',
                latitude=40.7614,
                longitude=-73.9776
            )
        ]
        for stadium in stadiums:
            db.session.add(stadium)
        
        db.session.commit()
        
        # Create sample events
        events = [
            Event(
                name='Championship Football Match',
                description='The final match of the season between top teams.',
                stadium_id=1,
                category_id=1,
                organizer_id=organizer.id,
                time_slot_id=1,
                price=50.00,
                available_tickets=1000,
                status='upcoming'
            ),
            Event(
                name='Summer Music Festival',
                description='Three days of non-stop music with top artists.',
                stadium_id=2,
                category_id=2,
                organizer_id=organizer.id,
                time_slot_id=2,
                price=150.00,
                available_tickets=500,
                status='upcoming'
            ),
            Event(
                name='Tech Conference 2024',
                description='Annual technology conference with industry leaders.',
                stadium_id=3,
                category_id=3,
                organizer_id=organizer.id,
                time_slot_id=3,
                price=200.00,
                available_tickets=200,
                status='upcoming'
            ),
            Event(
                name='Art Exhibition',
                description='Contemporary art exhibition featuring local artists.',
                stadium_id=4,
                category_id=4,
                organizer_id=organizer.id,
                time_slot_id=4,
                price=25.00,
                available_tickets=300,
                status='upcoming'
            ),
            Event(
                name='Broadway Show',
                description='Award-winning musical performance.',
                stadium_id=5,
                category_id=5,
                organizer_id=organizer.id,
                time_slot_id=5,
                price=75.00,
                available_tickets=100,
                status='upcoming'
            )
        ]
        
        # Create time slots for events
        base_date = datetime.now() + timedelta(days=7)  # Start events 7 days from now
        time_slots = []
        for i in range(5):
            start_time = base_date + timedelta(days=i*2)  # Events every 2 days
            end_time = start_time + timedelta(hours=3)
            time_slot = TimeSlot(
                start_time=start_time,
                end_time=end_time,
                is_available=True
            )
            time_slots.append(time_slot)
            db.session.add(time_slot)
        
        db.session.commit()
        
        # Assign time slots to events
        for i, event in enumerate(events):
            event.time_slot_id = time_slots[i].id
            db.session.add(event)
        
        # Create some sample bookings
        bookings = [
            Booking(
                user_id=customer.id,
                event_id=1,
                quantity=2,
                total_price=100.00,
                status='confirmed'
            ),
            Booking(
                user_id=customer.id,
                event_id=2,
                quantity=1,
                total_price=150.00,
                status='confirmed'
            )
        ]
        for booking in bookings:
            db.session.add(booking)
        
        # Create some sample reviews
        reviews = [
            Review(
                user_id=customer.id,
                stadium_id=1,
                rating=5,
                comment='Excellent venue with great facilities!',
                created_at=datetime.now()
            ),
            Review(
                user_id=customer.id,
                stadium_id=2,
                rating=4,
                comment='Good sound system and comfortable seating.',
                created_at=datetime.now()
            )
        ]
        for review in reviews:
            db.session.add(review)
        
        # Create some sample weather data
        weather_data = [
            Weather(
                stadium_id=1,
                date=datetime.now().date(),
                temperature=25.0,
                condition='Sunny',
                humidity=60,
                wind_speed=10.0
            ),
            Weather(
                stadium_id=2,
                date=datetime.now().date(),
                temperature=22.0,
                condition='Cloudy',
                humidity=70,
                wind_speed=8.0
            )
        ]
        for weather in weather_data:
            db.session.add(weather)
        
        db.session.commit()
        print("Sample data added to the existing database!")

if __name__ == '__main__':
    init_db() 