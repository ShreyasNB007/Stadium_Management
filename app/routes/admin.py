from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Stadium, Event, Booking, db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stadiums = Stadium.query.all()
    events = Event.query.all()
    tickets = Booking.query.all()
    return render_template('admin/dashboard.html', stadiums=stadiums, events=events, tickets=tickets)

@bp.route('/events')
@login_required
@admin_required
def events():
    # Get filter parameters
    status = request.args.get('status', 'pending')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Base query
    query = Event.query
    
    # Apply status filter
    if status in ['pending', 'approved', 'rejected']:
        query = query.filter_by(status=status)
    
    # Order by creation date
    query = query.order_by(Event.created_at.desc())
    
    # Paginate results
    events = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/events.html',
                         events=events,
                         current_status=status)

@bp.route('/events/<int:id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_event(id):
    event = Event.query.get_or_404(id)
    
    # Check if event is in pending state
    if event.status != 'pending':
        flash('Only pending events can be approved', 'danger')
        return redirect(url_for('admin.events'))
    
    try:
        if event.approve():
            db.session.commit()
            flash('Event approved successfully', 'success')
        else:
            flash('Event could not be approved', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error approving event: {str(e)}', 'danger')
    
    return redirect(url_for('admin.events'))

@bp.route('/events/<int:id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_event(id):
    event = Event.query.get_or_404(id)
    
    # Check if event is in pending state
    if event.status != 'pending':
        flash('Only pending events can be rejected', 'danger')
        return redirect(url_for('admin.events'))
    
    try:
        if event.reject():
            db.session.commit()
            flash('Event rejected successfully', 'success')
        else:
            flash('Event could not be rejected', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error rejecting event: {str(e)}', 'danger')
    
    return redirect(url_for('admin.events'))

@bp.route('/events/<int:id>/view')
@login_required
@admin_required
def view_event(id):
    event = Event.query.get_or_404(id)
    return render_template('admin/view_event.html', event=event)

@bp.route('/events/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_event(id):
    try:
        if request.method != 'POST':
            flash('Invalid request method.', 'danger')
            return redirect(url_for('admin.events'))
        if 'csrf_token' not in request.form:
            flash('CSRF token missing.', 'danger')
            return redirect(url_for('admin.events'))
        event = Event.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted.', 'danger')
    except Exception as e:
        import traceback
        print('Delete event error:', traceback.format_exc())
        flash(f'Error deleting event: {str(e)}', 'danger')
    return redirect(url_for('admin.events'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/stadiums/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_stadium():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        capacity = request.form['capacity']
        facilities = request.form['facilities']
        price_per_hour = request.form['price_per_hour']
        contact_info = request.form.get('contact_info')
        
        # Handle image upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_url = filename
        
        stadium = Stadium(
            name=name,
            location=location,
            capacity=capacity,
            facilities=facilities,
            price_per_hour=price_per_hour,
            contact_info=contact_info,
            image_url=image_url
        )
        
        db.session.add(stadium)
        db.session.commit()
        flash('Stadium created successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/create_stadium.html')

@bp.route('/stadiums/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_stadium(id):
    stadium = Stadium.query.get_or_404(id)
    
    if request.method == 'POST':
        stadium.name = request.form['name']
        stadium.location = request.form['location']
        stadium.capacity = request.form['capacity']
        stadium.facilities = request.form['facilities']
        stadium.price_per_hour = request.form['price_per_hour']
        stadium.contact_info = request.form.get('contact_info')
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                stadium.image_url = filename
        
        db.session.commit()
        flash('Stadium updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_stadium.html', stadium=stadium)

@bp.route('/stadiums/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_stadium(id):
    try:
        stadium = Stadium.query.get_or_404(id)
        
        # Check if stadium can be deleted
        can_delete, message = stadium.can_be_deleted()
        if not can_delete:
            flash(message, 'danger')
            return redirect(url_for('admin.stadiums'))
        
        # If no active events, proceed with deletion
        # This will cascade delete all associated records (time slots, events, reviews, weather)
        db.session.delete(stadium)
        db.session.commit()
        flash('Stadium and all associated records deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting stadium: {str(e)}', 'danger')
    
    return redirect(url_for('admin.stadiums'))

@bp.route('/stadiums')
@login_required
@admin_required
def stadiums():
    stadiums = Stadium.query.all()
    return render_template('admin/stadiums.html', stadiums=stadiums)

@bp.route('/stadiums/<int:id>')
@login_required
@admin_required
def view_stadium(id):
    stadium = Stadium.query.get_or_404(id)
    time_slots = stadium.time_slots
    events = stadium.events
    return render_template('admin/stadium_details.html', 
                         stadium=stadium, 
                         time_slots=time_slots, 
                         events=events)

@bp.route('/stadiums/<int:id>/manage', methods=['POST'])
@login_required
@admin_required
def manage_stadium_records(id):
    try:
        stadium = Stadium.query.get_or_404(id)
        action = request.form.get('action')
        
        if action == 'delete_time_slots':
            # Delete all time slots that don't have associated events
            for slot in stadium.time_slots:
                if not slot.events.first():
                    db.session.delete(slot)
            db.session.commit()
            flash('Available time slots deleted successfully.', 'success')
            
        elif action == 'delete_events':
            # Delete all events and their associated time slots
            for event in stadium.events:
                # Delete the event's time slot if it's not used by other events
                if event.time_slot and not event.time_slot.events.filter(Event.id != event.id).first():
                    db.session.delete(event.time_slot)
                db.session.delete(event)
            db.session.commit()
            flash('Events and associated time slots deleted successfully.', 'success')
            
        else:
            flash('Invalid action specified.', 'danger')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error managing stadium records: {str(e)}', 'danger')
    
    return redirect(url_for('admin.view_stadium', id=id)) 