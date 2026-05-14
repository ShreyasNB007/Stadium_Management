from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from app.models import Stadium, Event, Booking, Category
from app import db
from flask_login import login_required, current_user
import io
from datetime import datetime
from reportlab.pdfgen import canvas
import random
import string

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Get search parameters
    search = request.args.get('search', '')
    category_id = request.args.get('category')
    
    # Base queries
    stadiums_query = Stadium.query
    events_query = Event.query.filter_by(status='approved')  # Only show approved events
    
    # Apply search filter if provided
    if search:
        stadiums_query = stadiums_query.filter(
            (Stadium.name.ilike(f'%{search}%')) |
            (Stadium.location.ilike(f'%{search}%'))
        )
        events_query = events_query.filter(
            (Event.name.ilike(f'%{search}%')) |
            (Event.description.ilike(f'%{search}%'))
        )
    
    # Apply category filter if provided
    if category_id:
        events_query = events_query.filter_by(category_id=category_id)
    
    # Get stadiums and events
    stadiums = stadiums_query.all()
    upcoming_events = events_query.order_by(Event.created_at.desc()).limit(6).all()
    
    # Get a few stadiums to display on the homepage
    featured_stadiums = Stadium.query.limit(6).all()
    
    # Get categories for filter
    categories = Category.query.order_by(Category.name).all()
    
    # Get stats
    total_events = Event.query.filter_by(status='approved').count()  # Only count approved events
    total_stadiums = Stadium.query.count()
    total_bookings = Booking.query.filter(Booking.status == 'confirmed').count()  # Count confirmed bookings
    
    # Handle newsletter subscription
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # TODO: Implement newsletter subscription
            flash('Thank you for subscribing to our newsletter!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('index.html',
                         stadiums=stadiums,
                         upcoming_events=upcoming_events,
                         categories=categories,
                         selected_category=category_id,
                         total_events=total_events,
                         total_stadiums=total_stadiums,
                         total_bookings=total_bookings,
                         now=datetime.utcnow(),
                         featured_stadiums=featured_stadiums)

@bp.route('/events')
def events():
    # Get search parameters
    search = request.args.get('search', '')
    category_id = request.args.get('category')
    
    # Base query - start with Event model
    events_query = Event.query.filter_by(status='approved')  # Only show approved events
    
    # Apply search filter if provided
    if search:
        search_term = f'%{search}%'
        events_query = events_query.filter(
            (Event.name.ilike(search_term)) |
            (Event.description.ilike(search_term)) |
            (Event.stadium.has(Stadium.name.ilike(search_term))) |
            (Event.stadium.has(Stadium.location.ilike(search_term)))
        )
    
    # Apply category filter if provided
    if category_id:
        events_query = events_query.filter_by(category_id=category_id)
    
    # Get events ordered by creation date
    events = events_query.order_by(Event.created_at.desc()).all()
    
    # Get categories for filter
    categories = Category.query.order_by(Category.name).all()
    
    return render_template('events.html',
                         events=events,
                         categories=categories,
                         selected_category=category_id,
                         search=search,  # Pass search term back to template
                         now=datetime.utcnow())

@bp.route('/events/<int:event_id>/book', methods=['GET', 'POST'])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if event is approved
    if event.status != 'approved':
        flash('This event is not available for booking yet.', 'danger')
        return redirect(url_for('main.events'))
    
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        # Generate random seat number and stand
        seat_no = f"{random.choice(string.ascii_uppercase)}{random.randint(1, 50)}"
        stand = random.choice(['North', 'South', 'East', 'West'])
        if quantity < 1 or quantity > event.available_tickets:
            flash('Invalid ticket quantity.', 'danger')
            return redirect(url_for('main.book_event', event_id=event_id))
        
        booking = Booking(
            user_id=current_user.id,
            event_id=event.id,
            quantity=quantity,
            status='confirmed',
            seat_no=seat_no,
            stand=stand
        )
        event.available_tickets -= quantity
        db.session.add(booking)
        db.session.commit()
        flash('Tickets booked successfully!', 'success')
        return redirect(url_for('main.my_tickets'))
    return render_template('book_event.html', event=event)

@bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Ensure the booking belongs to the current user and is in a cancellable state
    if booking.user_id != current_user.id or booking.status != 'confirmed':
        flash('You cannot cancel this booking.', 'danger')
        return redirect(url_for('main.my_tickets'))

    try:
        # Update booking status
        booking.status = 'cancelled'

        # Increase available tickets for the event
        if booking.event:
            booking.event.available_tickets += booking.quantity
        
        db.session.commit()
        flash('Booking cancelled successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error cancelling booking: {str(e)}', 'danger')

    return redirect(url_for('main.my_tickets'))

@bp.route('/download-ticket/<int:booking_id>')
@login_required
def download_ticket(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id or booking.status != 'confirmed':
        flash('You cannot download this ticket.', 'danger')
        return redirect(url_for('main.my_tickets'))
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Ticket for {booking.event.name}")
    p.drawString(100, 780, f"Date: {booking.event.created_at.strftime('%Y-%m-%d')}")
    p.drawString(100, 760, f"Stadium: {booking.event.stadium.name}")
    p.drawString(100, 740, f"Quantity: {booking.quantity}")
    p.drawString(100, 720, f"Status: {booking.status.capitalize()}")
    p.drawString(100, 700, f"Seat No: {booking.seat_no}")
    p.drawString(100, 680, f"Stand: {booking.stand}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"ticket_{booking.id}.pdf", mimetype='application/pdf')

@bp.route('/my-tickets')
@login_required
def my_tickets():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template('my_tickets.html', tickets=bookings, now=datetime.utcnow())

@bp.route('/stadiums')
def stadiums():
    # Get search parameters
    search = request.args.get('search', '')
    
    # Base query
    stadiums_query = Stadium.query
    
    # Apply search filter if provided
    if search:
        stadiums_query = stadiums_query.filter(
            (Stadium.name.ilike(f'%{search}%')) |
            (Stadium.location.ilike(f'%{search}%'))
        )
    
    # Get stadiums
    stadiums = stadiums_query.all()
    
    return render_template('stadiums.html',
                         stadiums=stadiums,
                         search=search) 