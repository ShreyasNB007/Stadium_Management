from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFError

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            remember = request.form.get('remember', False)
            
            if not username or not password:
                flash('Please enter both username and password.', 'danger')
                return render_template('auth/login.html')
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                if not next_page or not next_page.startswith('/'):
                    next_page = url_for('main.index')
                return redirect(next_page)
            else:
                flash('Invalid username or password.', 'danger')
        except CSRFError:
            flash('The form submission was invalid. Please try again.', 'danger')
        except Exception as e:
            flash('An error occurred. Please try again.', 'danger')
            print(f"Login error: {str(e)}")
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            
            if not all([username, email, password, role]):
                flash('Please fill in all fields.', 'danger')
                return render_template('auth/register.html')
            
            if role not in ['admin', 'organizer', 'customer']:
                flash('Invalid role selected.', 'danger')
                return render_template('auth/register.html')
            
            if User.query.filter((User.username == username) | (User.email == email)).first():
                flash('Username or email already exists.', 'danger')
                return render_template('auth/register.html')
            
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except CSRFError:
            flash('The form submission was invalid. Please try again.', 'danger')
        except Exception as e:
            flash('An error occurred. Please try again.', 'danger')
            print(f"Registration error: {str(e)}")
    
    return render_template('auth/register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index')) 