from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Stadium, Event, Category, Booking, TimeSlot
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
from app.decorators import organizer_required

bp = Blueprint('organizer', __name__, url_prefix='/organizer')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'event_thumbnails')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/dashboard')
@login_required
@organizer_required
def dashboard():
    events = Event.query.filter_by(organizer_id=current_user.id).order_by(Event.created_at.desc()).all()
    stadiums = Stadium.query.all()
    return render_template('organizer/dashboard.html', events=events, stadiums=stadiums)

@bp.route('/create-event', methods=['GET', 'POST'])
@login_required
@organizer_required
def create_event():
    if request.method == 'POST':
        try:
            # Parse date and time
            event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()
            event_time = datetime.strptime(request.form['event_time'], '%H:%M').time()
            duration_hours = int(request.form['duration_hours'])
            
            # Check if the time slot is available
            start_datetime = datetime.combine(event_date, event_time)
            end_datetime = start_datetime + timedelta(hours=duration_hours)
            
            # Check for overlapping events in the selected stadium
            stadium_id = int(request.form['stadium_id'])
            overlapping_events = Event.query.join(Event.time_slot).filter(
                Event.stadium_id == stadium_id,
                Event.status != 'rejected',
                TimeSlot.start_time < end_datetime,
                TimeSlot.end_time > start_datetime
            ).first()
            
            if overlapping_events:
                flash('This time slot is already booked for the selected stadium. Please choose a different time or stadium.', 'danger')
                return redirect(url_for('organizer.create_event'))
            
            # Create the event
            event = Event(
                name=request.form['name'],
                description=request.form['description'],
                total_tickets=int(request.form['total_tickets']),
                available_tickets=int(request.form['total_tickets']),
                stadium_id=stadium_id,
                organizer_id=current_user.id,
                category_id=request.form.get('category_id'),
                event_date=event_date,
                event_time=event_time,
                duration_hours=duration_hours
            )
            
            # Handle thumbnail upload
            if 'thumbnail' in request.files:
                file = request.files['thumbnail']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    event.thumbnail = filename
            
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('organizer.dashboard'))
            
        except ValueError as e:
            flash(f'Invalid date or time format: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}', 'danger')
            
    stadiums = Stadium.query.all()
    categories = Category.query.all()
    return render_template('organizer/create_event.html', 
                         stadiums=stadiums, 
                         categories=categories,
                         now=datetime.utcnow())

@bp.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
@organizer_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if event.organizer_id != current_user.id:
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('organizer.dashboard'))
        
    if not event.can_be_edited():
        flash('This event cannot be edited as it has been approved.', 'warning')
        return redirect(url_for('organizer.dashboard'))
    
    if request.method == 'POST':
        try:
            event.name = request.form['name']
            event.description = request.form['description']
            event.total_tickets = int(request.form['total_tickets'])
            event.available_tickets = int(request.form['total_tickets'])
            event.stadium_id = int(request.form['stadium_id'])
            event.category_id = request.form.get('category_id')
            
            if 'thumbnail' in request.files:
                file = request.files['thumbnail']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    event.thumbnail = filename
            
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('organizer.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating event: {str(e)}', 'danger')
    
    stadiums = Stadium.query.all()
    categories = Category.query.all()
    return render_template('organizer/edit_event.html', event=event, stadiums=stadiums, categories=categories)

@bp.route('/delete-event/<int:event_id>', methods=['POST'])
@login_required
@organizer_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if event.organizer_id != current_user.id:
        flash('You do not have permission to delete this event.', 'danger')
        return redirect(url_for('organizer.dashboard'))
        
    if not event.can_be_edited():
        flash('This event cannot be deleted as it has been approved.', 'warning')
        return redirect(url_for('organizer.dashboard'))
    
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'danger')
    
    return redirect(url_for('organizer.dashboard'))

@bp.route('/api/events/<int:id>')
@login_required
@organizer_required
def get_event_details(id):
    event = Event.query.get_or_404(id)
    
    if event.organizer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'category': event.category.name if event.category else None,
        'status': event.status,
        'total_tickets': event.total_tickets,
        'available_tickets': event.available_tickets,
        'stadium': {
            'id': event.stadium.id,
            'name': event.stadium.name,
            'location': event.stadium.location
        }
    }) 