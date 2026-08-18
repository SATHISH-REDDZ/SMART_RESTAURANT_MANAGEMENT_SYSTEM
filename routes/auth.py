from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('customer.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Please provide both email and password.', 'warning')
            return render_template('auth/login.html')

        user = User.find_by_email(email)
        if user and User.verify_password(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['email'] = user['email']
            session['role'] = user['role']

            flash(f"Welcome back, {user['name']}!", 'success')
            
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)

            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('customer.home'))

        flash('Invalid email address or password.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('customer.home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if not name or not email or not password:
            flash('Name, Email, and Password are required.', 'warning')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'warning')
            return render_template('auth/register.html')

        existing_user = User.find_by_email(email)
        if existing_user:
            flash('An account with this email already exists.', 'danger')
            return render_template('auth/register.html')

        user_id = User.create(name, email, password, phone, address, role='customer')
        if user_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

        flash('An error occurred during registration. Please try again.', 'danger')

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('auth.login'))
