from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
try:
    from flask_mail import Mail, Message
    MAIL_ENABLED = True
except ImportError:
    MAIL_ENABLED = False
    print("Flask-Mail not available. Email notifications disabled.")
import sqlite3
import os
import re
import random
import secrets
import string
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging for production
if os.environ.get('FLASK_ENV') == 'production':
    logging.basicConfig(
        filename='startsmart.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
else:
    logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2025'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Production Security Settings
if os.environ.get('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Custom Jinja2 filters
@app.template_filter('datetime')
def datetime_filter(value, format='%b %d, %Y'):
    """Convert a datetime string or object to formatted string"""
    if value is None:
        return 'Recently'
    
    if isinstance(value, str):
        try:
            # Try different datetime string formats
            try:
                dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                try:
                    dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return 'Recently'
        except:
            return 'Recently'
    elif hasattr(value, 'strftime'):
        dt = value
    else:
        return 'Recently'
    
    return dt.strftime(format)

@app.template_filter('nl2br')
def nl2br_filter(value):
    """Convert newlines to <br> tags"""
    if value is None:
        return ''
    return value.replace('\n', '<br>')

# Email configuration
if MAIL_ENABLED:
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') or 'j.kur@alustudent.com'
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS') or 'your-app-password'
    app.config['MAIL_DEFAULT_SENDER'] = 'StartSmart Platform <j.kur@alustudent.com>'
    mail = Mail(app)
else:
    mail = None

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# File upload helper function
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Error Handlers for Production
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', 
                         error_code=403, 
                         error_message="Access forbidden"), 403

# Email notification functions
def send_email(to_email, subject, body, html_body=None):
    if not MAIL_ENABLED or not mail:
        print(f"📧 Email notification: {subject} to {to_email}")
        return False
    try:
        msg = Message(subject, recipients=[to_email])
        msg.body = body
        if html_body:
            msg.html = html_body
        mail.send(msg)
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

def notify_new_job(job_title, company):
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE user_type = 'student'")
    students = c.fetchall()
    conn.close()
    
    subject = f"New Job Opportunity: {job_title}"
    body = f"A new job opportunity has been posted:\n\nPosition: {job_title}\nCompany: {company}\n\nVisit StartSmart to apply now!"
    
    for student in students:
        send_email(student[0], subject, body)

def notify_application_status(student_email, job_title, status):
    subject = f"Application Update: {job_title}"
    body = f"Your application status has been updated:\n\nJob: {job_title}\nStatus: {status.title()}\n\nLogin to StartSmart for more details."
    send_email(student_email, subject, body)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text):
    if text is None:
        return ''
    return str(text).strip()[:500]

def generate_reset_token():
    """Generate secure password reset token"""
    return secrets.token_urlsafe(32)

def create_reset_token(user_id):
    """Create password reset token for user"""
    token = generate_reset_token()
    expires_at = datetime.now() + timedelta(minutes=30)
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Invalidate old tokens
    c.execute("UPDATE password_reset_tokens SET used = 1 WHERE user_id = ?", (user_id,))
    
    # Create new token
    c.execute("INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
              (user_id, token, expires_at))
    
    conn.commit()
    conn.close()
    return token

def validate_reset_token(token):
    """Validate password reset token"""
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute("""SELECT user_id FROM password_reset_tokens 
                 WHERE token = ? AND used = 0 AND expires_at > ?""",
              (token, datetime.now()))
    
    result = c.fetchone()
    conn.close()
    
    return result[0] if result else None

def init_db():
    from db_setup import setup_database
    setup_database()
    
    # Add password reset table
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM users")
    user_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM jobs")
    job_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM startups")
    startup_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users WHERE user_type = 'mentor'")
    mentor_count = c.fetchone()[0]
    
    c.execute("""SELECT id, title, company, description, location, job_type, salary, 
                 application_url, created_at FROM jobs 
                 WHERE is_active = 1
                 ORDER BY created_at DESC LIMIT 4""")
    recent_jobs_raw = c.fetchall()
    
    # Convert datetime strings to datetime objects
    recent_jobs = []
    for job in recent_jobs_raw:
        job_dict = list(job)
        # job[8] is the created_at field
        if job_dict[8] and isinstance(job_dict[8], str):
            try:
                job_dict[8] = datetime.strptime(job_dict[8], '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                try:
                    job_dict[8] = datetime.strptime(job_dict[8], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    job_dict[8] = None
        recent_jobs.append(tuple(job_dict))
    
    job_skills = {}
    for job in recent_jobs:
        c.execute("""SELECT s.name FROM skills s 
                     JOIN job_skills js ON s.id = js.skill_id 
                     WHERE js.job_id = ? LIMIT 3""", (job[0],))
        skills = [skill[0] for skill in c.fetchall()]
        job_skills[job[0]] = skills
    
    c.execute("""SELECT id, name, description, industry, founder_id 
                 FROM startups ORDER BY created_at DESC LIMIT 3""")
    featured_startups = c.fetchall()
    
    founder_names = {}
    founder_images = {}
    for startup in featured_startups:
        founder_id = startup[4]  # founder_id is now at index 4 (was 5 when stage column existed)
        c.execute("SELECT name, profile_image FROM users WHERE id = ?", (founder_id,))
        founder = c.fetchone()
        if founder:
            founder_names[founder_id] = founder[0]
            founder_images[founder_id] = founder[1] if founder[1] else 'default-profile.jpg'
    
    conn.close()
    
    stats = {
        'users': user_count,
        'jobs': job_count,
        'startups': startup_count,
        'mentors': mentor_count
    }
    
    return render_template('index.html', 
                          stats=stats,
                          recent_jobs=recent_jobs,
                          job_skills=job_skills,
                          featured_startups=featured_startups,
                          founder_names=founder_names,
                          founder_images=founder_images)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connectivity
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        conn.close()
        
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'users': user_count
        }, 200
    except Exception as e:
        app.logger.error(f"Health check failed: {str(e)}")
        return {
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }, 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        # Get and sanitize form data
        email = sanitize_input(request.form.get('email', '')).lower().strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        name = sanitize_input(request.form.get('name', ''))
        user_type = request.form.get('user_type', '')

        # Comprehensive validation
        errors = []

        # Name validation
        if not name or len(name.strip()) < 2:
            errors.append('Please enter a valid full name (at least 2 characters)')
        elif len(name) > 100:
            errors.append('Name must be less than 100 characters')
        elif not re.match(r'^[a-zA-Z\s\'-\.]+$', name):
            errors.append('Name can only contain letters, spaces, hyphens, apostrophes, and periods')

        # Email validation
        if not email:
            errors.append('Email address is required')
        elif not validate_email(email):
            errors.append('Please enter a valid email address')
        elif len(email) > 254:
            errors.append('Email address is too long')

        # Password validation
        if not password:
            errors.append('Password is required')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        elif len(password) > 128:
            errors.append('Password must be less than 128 characters')
        else:
            # Advanced password strength validation
            password_checks = {
                'lowercase': re.search(r"[a-z]", password),
                'uppercase': re.search(r"[A-Z]", password),
                'digit': re.search(r"\d", password),
                'special': re.search(r"[@$!%*?&#^()_+=\-\[\]{}|\\:;\"'<>,.?/~`]", password)
            }
            
            missing_requirements = []
            if not password_checks['lowercase']:
                missing_requirements.append('lowercase letter')
            if not password_checks['uppercase']:
                missing_requirements.append('uppercase letter')
            if not password_checks['digit']:
                missing_requirements.append('number')
            if not password_checks['special']:
                missing_requirements.append('special character')
            
            if missing_requirements:
                errors.append(f'Password must contain at least one: {", ".join(missing_requirements)}')

        # Password confirmation
        if password != confirm_password:
            errors.append('Passwords do not match')

        # User type validation
        valid_user_types = ['student', 'mentor', 'recruiter']
        if user_type not in valid_user_types:
            errors.append('Please select a valid user type')

        # If there are validation errors, return with messages
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html', form_data=request.form)

        # Check for existing email before attempting registration
        conn = None
        try:
            conn = sqlite3.connect('startsmart.db')
            c = conn.cursor()

            # Check if email already exists
            c.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,))
            existing_user = c.fetchone()

            if existing_user:
                flash('An account with this email already exists. Please use a different email or try logging in.', 'error')
                return render_template('register.html', form_data=request.form)

            # Create password hash
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')

            # Insert new user with enhanced data
            c.execute("""INSERT INTO users (email, password, name, user_type, created_at, is_active) 
                         VALUES (?, ?, ?, ?, ?, ?)""",
                     (email, password_hash, name, user_type, datetime.now(), 1))
            conn.commit()

            new_user_id = c.lastrowid
            
            # Success message and redirect
            flash('Registration successful! Welcome to StartSmart. Please log in with your credentials.', 'success')
            print(f"✅ New user registered: {name} ({email}) - ID: {new_user_id}")
            
            # Optional: Send welcome email
            if MAIL_ENABLED:
                try:
                    welcome_subject = "Welcome to StartSmart!"
                    welcome_body = f"""Dear {name},

Welcome to StartSmart! Your account has been successfully created.

Account Details:
- Email: {email}
- Role: {user_type.title()}

You can now log in and start exploring opportunities, connecting with mentors, and building your career in Africa.

Best regards,
The StartSmart Team"""
                    send_email(email, welcome_subject, welcome_body)
                except Exception as e:
                    print(f"Welcome email failed: {e}")
            
            return redirect(url_for('login'))

        except sqlite3.Error as e:
            flash('A database error occurred. Please try again later.', 'error')
            print(f"❌ Database error during registration: {e}")
            return render_template('register.html', form_data=request.form)
        except Exception as e:
            flash('Registration failed due to an unexpected error. Please try again.', 'error')
            print(f"❌ Unexpected error during registration: {e}")
            return render_template('register.html', form_data=request.form)
        finally:
            if conn:
                conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = sanitize_input(request.form.get('email', '')).lower().strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('rememberMe')

        # Validation
        errors = []
        if not email:
            errors.append('Email is required!')
        elif not validate_email(email):
            errors.append('Please enter a valid email address!')
        
        if not password:
            errors.append('Password is required!')
        
        if errors:
            for error in errors:
                flash(error)
            return render_template('login.html', form_data=request.form)
        
        conn = None
        try:
            conn = sqlite3.connect('startsmart.db')
            c = conn.cursor()
            c.execute("SELECT id, name, password, email, user_type FROM users WHERE LOWER(email) = ?", (email,))
            user = c.fetchone()
            
            if user and check_password_hash(user[2], password):
                # Successful login
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                session['user_email'] = user[3]
                session['user_type'] = user[4]
                
                if remember_me:
                    session.permanent = True
                
                # Update last login
                try:
                    c.execute("UPDATE users SET last_login = ? WHERE id = ?", 
                             (datetime.now(), user[0]))
                    conn.commit()
                except sqlite3.Error as e:
                    print(f"⚠️ Could not update last_login: {e}")

                flash(f'Welcome back, {user[1]}!')
                print(f"✅ User logged in: {user[1]} ({email})")
                
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            else:
                flash('Invalid email or password. Please try again.')
                return render_template('login.html', form_data=request.form)

        except sqlite3.Error as e:
            flash('Database error occurred. Please try again.')
            print(f"❌ Database error during login: {e}")
            return render_template('login.html', form_data=request.form)
        except Exception as e:
            flash('Login failed. Please try again.')
            print(f"❌ General error during login: {e}")
            return render_template('login.html', form_data=request.form)
        finally:
            if conn:
                conn.close()
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute("SELECT name, user_type FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    
    dashboard_data = {'user': user}
    
    c.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0", (session['user_id'],))
    unread_notifications = c.fetchone()[0]
    dashboard_data['unread_notifications'] = unread_notifications

    if session['user_type'] == 'student':
        c.execute("SELECT COUNT(*) FROM applications WHERE user_id = ?", (session['user_id'],))
        total_applications = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM applications WHERE user_id = ? AND status = 'pending'", (session['user_id'],))
        pending_applications = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM applications WHERE user_id = ? AND status = 'shortlisted'", (session['user_id'],))
        shortlisted_applications = c.fetchone()[0]
        
        c.execute("""SELECT j.title, j.company, a.status, a.applied_at 
                     FROM applications a JOIN jobs j ON a.job_id = j.id 
                     WHERE a.user_id = ? ORDER BY a.applied_at DESC LIMIT 5""", (session['user_id'],))
        recent_applications_raw = c.fetchall()
        
        # Convert datetime strings to datetime objects
        recent_applications = []
        for app in recent_applications_raw:
            app_dict = list(app)
            # app[3] is the applied_at field
            if app_dict[3] and isinstance(app_dict[3], str):
                try:
                    app_dict[3] = datetime.strptime(app_dict[3], '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    try:
                        app_dict[3] = datetime.strptime(app_dict[3], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        app_dict[3] = None
            recent_applications.append(tuple(app_dict))
        
        dashboard_data.update({
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'shortlisted_applications': shortlisted_applications,
            'recent_applications': recent_applications
        })
    
    elif session['user_type'] == 'recruiter':
        c.execute("SELECT COUNT(*) FROM jobs WHERE posted_by = ?", (session['user_id'],))
        total_jobs = c.fetchone()[0]
        
        c.execute("""SELECT COUNT(*) FROM applications a 
                     JOIN jobs j ON a.job_id = j.id 
                     WHERE j.posted_by = ?""", (session['user_id'],))
        total_applications = c.fetchone()[0]
        
        c.execute("SELECT title, company, created_at FROM jobs WHERE posted_by = ? ORDER BY created_at DESC LIMIT 5", (session['user_id'],))
        recent_jobs_raw = c.fetchall()
        
        # Convert datetime strings to datetime objects
        recent_jobs = []
        for job in recent_jobs_raw:
            job_dict = list(job)
            # job[2] is the created_at field
            if job_dict[2] and isinstance(job_dict[2], str):
                try:
                    job_dict[2] = datetime.strptime(job_dict[2], '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    try:
                        job_dict[2] = datetime.strptime(job_dict[2], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        job_dict[2] = None
            recent_jobs.append(tuple(job_dict))
        
        dashboard_data.update({
            'total_jobs': total_jobs,
            'total_applications': total_applications,
            'recent_jobs': recent_jobs
        })
    
    conn.close()
    return render_template('dashboard.html', **dashboard_data)

@app.route('/live-analytics')
def live_analytics():
    """Live analytics dashboard for presentations"""
    # Remove login restriction for demo purposes
    # if 'user_id' not in session:
    #     return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get real platform statistics
    c.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
    active_users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1")
    total_jobs = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM applications")
    total_applications = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM startups")
    total_startups = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users WHERE user_type = 'mentor'")
    total_mentors = c.fetchone()[0]
    
    # Get recent activity
    c.execute("""
        SELECT 'New User' as type, name as title, created_at 
        FROM users 
        WHERE created_at >= datetime('now', '-7 days')
        UNION ALL
        SELECT 'Job Posted' as type, title, created_at 
        FROM jobs 
        WHERE created_at >= datetime('now', '-7 days')
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    recent_activity = c.fetchall()
    
    conn.close()
    
    analytics_data = {
        'active_users': active_users,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_startups': total_startups,
        'total_mentors': total_mentors,
        'recent_activity': recent_activity
    }
    
    return render_template('live_analytics.html', analytics=analytics_data)

@app.route('/job/<int:job_id>')
def view_job(job_id):
    """View detailed information about a specific job"""
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get job details with recruiter information
    c.execute("""
        SELECT j.*, u.name as recruiter_name, u.email as recruiter_email 
        FROM jobs j 
        LEFT JOIN users u ON j.posted_by = u.id 
        WHERE j.id = ? AND j.is_active = 1
    """, (job_id,))
    
    job = c.fetchone()
    
    if not job:
        flash('Job not found or no longer available.', 'error')
        return redirect(url_for('jobs'))
    
    # Check if user has already applied (if logged in as student)
    has_applied = False
    if 'user_id' in session and session.get('user_type') == 'student':
        c.execute("SELECT 1 FROM applications WHERE user_id = ? AND job_id = ?", 
                 (session['user_id'], job_id))
        application_check = c.fetchone()
        has_applied = application_check is not None
        print(f"Debug: User {session['user_id']} checking job {job_id}, has_applied: {has_applied}")
    
    # Get related jobs from the same company
    c.execute("""
        SELECT id, title, job_type, location, created_at 
        FROM jobs 
        WHERE company = ? AND id != ? AND is_active = 1 
        ORDER BY created_at DESC 
        LIMIT 3
    """, (job[2], job_id))
    
    related_jobs = c.fetchall()
    
    conn.close()
    
    return render_template('view_job.html', job=job, has_applied=has_applied, related_jobs=related_jobs)

@app.route('/apply-job/<int:job_id>')
def apply_job(job_id):
    """Show job application form or redirect to original posting"""
    if 'user_id' not in session:
        flash('Please login to apply for jobs.', 'error')
        return redirect(url_for('login'))
    
    if session.get('user_type') != 'student':
        flash('Only students can apply for jobs.', 'error')
        return redirect(url_for('view_job', job_id=job_id))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Check if job exists and is active
    c.execute("SELECT * FROM jobs WHERE id = ? AND is_active = 1", (job_id,))
    job = c.fetchone()
    
    if not job:
        flash('Job not found or no longer available.', 'error')
        conn.close()
        return redirect(url_for('jobs'))
    
    # If this is an imported job (posted_by = 1), redirect to original posting
    if job[7] == 1 and job[9]:  # posted_by = 1 and has application_url
        flash('Redirecting to the original job posting to apply directly with the company.', 'info')
        conn.close()
        return redirect(job[9])  # Redirect to application_url
    
    # Check if user has already applied
    c.execute("SELECT 1 FROM applications WHERE user_id = ? AND job_id = ?", 
             (session['user_id'], job_id))
    
    if c.fetchone():
        flash('You have already applied for this job.', 'warning')
        conn.close()
        return redirect(url_for('view_job', job_id=job_id))
    
    conn.close()
    return render_template('apply_job.html', job=job)

@app.route('/submit-application/<int:job_id>', methods=['POST'])
def submit_application(job_id):
    """Submit job application with details"""
    if 'user_id' not in session:
        flash('Please login to apply for jobs.', 'error')
        return redirect(url_for('login'))
    
    if session.get('user_type') != 'student':
        flash('Only students can apply for jobs.', 'error')
        return redirect(url_for('view_job', job_id=job_id))
    
    # Get form data
    cover_letter = sanitize_input(request.form.get('cover_letter', ''))
    relevant_experience = sanitize_input(request.form.get('relevant_experience', ''))
    portfolio_url = sanitize_input(request.form.get('portfolio_url', ''))
    availability = request.form.get('availability', '')
    
    # Validation
    if len(cover_letter) < 100:
        flash('Cover letter must be at least 100 characters long.', 'error')
        return redirect(url_for('apply_job', job_id=job_id))
    
    if len(relevant_experience) < 50:
        flash('Relevant experience must be at least 50 characters long.', 'error')
        return redirect(url_for('apply_job', job_id=job_id))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Check if job exists and is active
    c.execute("SELECT title, company FROM jobs WHERE id = ? AND is_active = 1", (job_id,))
    job = c.fetchone()
    
    if not job:
        flash('Job not found or no longer available.', 'error')
        conn.close()
        return redirect(url_for('jobs'))
    
    # Check if user has already applied
    c.execute("SELECT 1 FROM applications WHERE user_id = ? AND job_id = ?", 
             (session['user_id'], job_id))
    
    if c.fetchone():
        flash('You have already applied for this job.', 'warning')
        conn.close()
        return redirect(url_for('view_job', job_id=job_id))
    
    # Create detailed application
    c.execute("""
        INSERT INTO applications (user_id, job_id, status, applied_at, cover_letter, 
                                relevant_experience, portfolio_url)
        VALUES (?, ?, 'pending', ?, ?, ?, ?)
    """, (session['user_id'], job_id, datetime.now(), cover_letter, 
           relevant_experience, portfolio_url))
    
    conn.commit()
    conn.close()
    
    flash(f'Successfully applied for {job[0]} at {job[1]}! Your application has been submitted for review.', 'success')
    return redirect(url_for('view_job', job_id=job_id))

# ============ JOB APIs ============

@app.route('/api/jobs', methods=['GET'])
def api_get_jobs():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('job_type', '')
    limit = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []
    
    if search:
        query += " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])
    
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")
    
    if job_type:
        query += " AND job_type = ?"
        params.append(job_type)
    
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    c.execute(query, params)
    jobs = c.fetchall()
    
    count_query = "SELECT COUNT(*) FROM jobs WHERE 1=1"
    count_params = []
    if search:
        count_query += " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"
        count_params.extend([search_term, search_term, search_term])
    if location:
        count_query += " AND location LIKE ?"
        count_params.append(f"%{location}%")
    if job_type:
        count_query += " AND job_type = ?"
        count_params.append(job_type)
    
    c.execute(count_query, count_params)
    total = c.fetchone()[0]
    conn.close()
    
    jobs_list = []
    for job in jobs:
        jobs_list.append({
            'id': job[0],
            'title': job[1],
            'company': job[2],
            'description': job[3],
            'location': job[4],
            'salary': job[5],
            'job_type': job[6],
            'posted_by': job[7],
            'created_at': job[8],
            'application_url': job[9],
            'requirements': job[10],
            'benefits': job[11],
            'deadline': job[12]
        })
    
    return jsonify({
        'success': True,
        'jobs': jobs_list,
        'total': total,
        'limit': limit,
        'offset': offset
    })

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def api_get_job(job_id):
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = c.fetchone()
    conn.close()
    
    if not job:
        return jsonify({'success': False, 'message': 'Job not found'}), 404
    
    return jsonify({
        'success': True,
        'job': {
            'id': job[0],
            'title': job[1],
            'company': job[2],
            'description': job[3],
            'location': job[4],
            'salary': job[5],
            'job_type': job[6],
            'posted_by': job[7],
            'created_at': job[8],
            'application_url': job[9],
            'requirements': job[10],
            'benefits': job[11],
            'deadline': job[12]
        }
    })

@app.route('/api/jobs', methods=['POST'])
def api_create_job():
    if 'user_id' not in session or session['user_type'] != 'recruiter':
        return jsonify({'success': False, 'message': 'Only recruiters can post jobs'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    required_fields = ['title', 'company', 'description', 'location', 'job_type', 'requirements', 'application_url']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} is required'}), 400
    
    if data['job_type'] not in ['full-time', 'part-time', 'internship', 'contract', 'remote', 'hybrid']:
        return jsonify({'success': False, 'message': 'Invalid job type'}), 400
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO jobs (title, company, description, location, salary, job_type, 
                     posted_by, created_at, requirements, benefits, deadline, application_url) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                 (data['title'], data['company'], data['description'], data['location'],
                  data.get('salary'), data['job_type'], session['user_id'], datetime.now(),
                  data['requirements'], data.get('benefits'), data.get('deadline'), data['application_url']))
        job_id = c.lastrowid
        conn.commit()
        
        notify_new_job(data['title'], data['company'])
        
        return jsonify({
            'success': True,
            'message': 'Job created successfully',
            'job_id': job_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to create job'}), 500
    finally:
        conn.close()

@app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
def api_apply_job(job_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 401
    
    if session.get('user_type') != 'student':
        return jsonify({'success': False, 'message': 'Only students can apply for jobs'}), 403
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute("SELECT title, company FROM jobs WHERE id = ?", (job_id,))
    job = c.fetchone()
    if not job:
        conn.close()
        return jsonify({'success': False, 'message': 'Job not found'}), 404
    
    c.execute("SELECT id FROM applications WHERE job_id = ? AND user_id = ?", 
             (job_id, session['user_id']))
    if c.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Already applied for this job'}), 400
    
    try:
        c.execute("INSERT INTO applications (job_id, user_id, applied_at) VALUES (?, ?, ?)",
                 (job_id, session['user_id'], datetime.now()))
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully applied for {job[0]} at {job[1]}'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to submit application'}), 500
    finally:
        conn.close()

# ============ WEB ROUTES ============

@app.route('/jobs')
def jobs():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('job_type', '')
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    query = "SELECT * FROM jobs WHERE is_active = 1"
    params = []
    
    if search:
        query += " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])
    
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")
    
    if job_type:
        query += " AND job_type = ?"
        params.append(job_type)
    
    query += " ORDER BY created_at DESC"
    
    c.execute(query, params)
    jobs_raw = c.fetchall()
    conn.close()
    
    # Convert datetime strings to datetime objects for proper template rendering
    jobs_list = []
    for job in jobs_raw:
        job_dict = list(job)
        # job[8] is the created_at field - ensure it's handled properly
        if job_dict[8]:
            # Always keep as string for the datetime filter to handle
            if not isinstance(job_dict[8], str):
                job_dict[8] = str(job_dict[8])
        jobs_list.append(tuple(job_dict))
    
    return render_template('jobs.html', jobs=jobs_list, search=search, location=location, job_type=job_type)

@app.route('/ai-job-matches')
def ai_job_matches():
    """AI-powered job matching for students"""
    if 'user_id' not in session:
        flash('Please log in to access AI job matches.')
        return redirect(url_for('login'))
    
    if session.get('user_type') != 'student':
        flash('AI job matching is only available for students.')
        return redirect(url_for('dashboard'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get user's skills and preferences
    c.execute("SELECT skills, location FROM users WHERE id = ?", (session['user_id'],))
    user_data = c.fetchone()
    
    # Get available jobs
    c.execute("""SELECT id, title, company, description, location, salary, 
                 job_type, requirements, created_at FROM jobs 
                 WHERE is_active = 1 ORDER BY created_at DESC""")
    jobs = c.fetchall()
    
    conn.close()
    
    # Simple AI matching logic based on skills and location
    user_skills = user_data[0].lower().split(',') if user_data[0] else []
    user_location = user_data[1].lower() if user_data[1] else ''
    
    matched_jobs = []
    for job in jobs:
        match_score = 0
        requirements = job[7].lower() if job[7] else ''
        job_location = job[4].lower() if job[4] else ''
        
        # Skill matching
        for skill in user_skills:
            if skill.strip() in requirements:
                match_score += 30
        
        # Location matching
        if user_location and user_location in job_location:
            match_score += 20
        
        # Job type preference (favor internships for students)
        if 'intern' in job[6].lower():
            match_score += 15
        
        if match_score > 0:
            matched_jobs.append((job, match_score))
    
    # Sort by match score
    matched_jobs.sort(key=lambda x: x[1], reverse=True)
    
    return render_template('ai_job_matches.html', matched_jobs=matched_jobs)

@app.route('/startups')
def startups():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM startups ORDER BY created_at DESC")
    startups_list = c.fetchall()
    conn.close()
    return render_template('startups.html', startups=startups_list)

@app.route('/mentorship')
def mentorship():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_type = 'mentor'")
    mentors = c.fetchall()
    conn.close()
    return render_template('mentorship.html', mentors=mentors)

@app.route('/resources')
def resources():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    query = "SELECT r.id, r.title, r.description, r.category, r.file_url, r.external_url, r.created_at, r.view_count, u.name as uploader_name FROM resources r LEFT JOIN users u ON r.uploaded_by = u.id WHERE 1=1"
    params = []
    
    if category:
        query += " AND r.category = ?"
        params.append(category)
    
    if search:
        query += " AND (r.title LIKE ? OR r.description LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])
    
    query += " ORDER BY r.created_at DESC"
    
    c.execute(query, params)
    resources_list = c.fetchall()
    
    # Get categories for filter with counts
    c.execute("SELECT category, COUNT(*) FROM resources WHERE category IS NOT NULL GROUP BY category")
    categories_data = c.fetchall()
    categories = [{'name': cat[0], 'count': cat[1]} for cat in categories_data]
    
    conn.close()
    return render_template('resources.html', resources=resources_list, categories=categories, 
                          selected_category=category, search=search)

@app.route('/upload-resource', methods=['GET', 'POST'])
def upload_resource():
    if 'user_id' not in session or session.get('user_type') not in ['mentor', 'admin']:
        flash('Only mentors and admins can upload resources!')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = sanitize_input(request.form.get('title', ''))
        description = sanitize_input(request.form.get('description', ''))
        category = request.form.get('category', '')
        external_url = sanitize_input(request.form.get('external_url', ''))
        
        if not title or not description or not category:
            flash('Please fill in all required fields!')
            return render_template('upload_resource.html')
        
        file_url = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Add timestamp to avoid naming conflicts
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_url = f"uploads/{filename}"
        
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        c.execute("""INSERT INTO resources 
                  (title, description, category, file_url, external_url, uploaded_by, created_at) 
                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
                 (title, description, category, file_url, external_url, session['user_id'], datetime.now()))
        
        conn.commit()
        conn.close()
        
        flash('Resource uploaded successfully!')
        return redirect(url_for('resources'))
    
    return render_template('upload_resource.html')

@app.route('/download-resource/<int:resource_id>')
def download_resource(resource_id):
    if 'user_id' not in session:
        flash('Please log in to access resources!')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get resource details
    c.execute("SELECT file_url, external_url, title, view_count FROM resources WHERE id = ?", (resource_id,))
    resource = c.fetchone()
    
    if not resource:
        flash('Resource not found!')
        return redirect(url_for('resources'))
    
    file_url, external_url, title, view_count = resource
    
    # Increment view count
    c.execute("UPDATE resources SET view_count = ? WHERE id = ?", (view_count + 1, resource_id))
    conn.commit()
    conn.close()
    
    # Redirect to external URL if available, otherwise try file download
    if external_url:
        return redirect(external_url)
    elif file_url:
        return redirect(url_for('static', filename=file_url))
    else:
        flash('No resource available!')
        return redirect(url_for('resources'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    
    applications = []
    if session['user_type'] == 'student':
        c.execute("""SELECT j.title, j.company, a.status, a.applied_at 
                     FROM applications a JOIN jobs j ON a.job_id = j.id 
                     WHERE a.user_id = ? ORDER BY a.applied_at DESC""", (session['user_id'],))
        applications = c.fetchall()
    
    conn.close()
    return render_template('profile.html', user=user, applications=applications)

@app.route('/my-applications')
def my_applications():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("""SELECT a.id, j.title, j.company, j.location, j.job_type, 
                        a.status, a.applied_at, j.id as job_id
                 FROM applications a 
                 JOIN jobs j ON a.job_id = j.id 
                 WHERE a.user_id = ? 
                 ORDER BY a.applied_at DESC""", (session['user_id'],))
    applications = c.fetchall()
    conn.close()
    
    return render_template('my_applications.html', applications=applications)

@app.route('/manage-applications')
def manage_applications():
    if 'user_id' not in session or session.get('user_type') != 'recruiter':
        flash('Only recruiters can manage applications!')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("""SELECT a.id, j.title, j.company, u.name, u.email, 
                        a.status, a.applied_at, u.id as user_id, j.id as job_id
                 FROM applications a 
                 JOIN jobs j ON a.job_id = j.id 
                 JOIN users u ON a.user_id = u.id
                 WHERE j.posted_by = ? 
                 ORDER BY a.applied_at DESC""", (session['user_id'],))
    applications = c.fetchall()
    conn.close()
    
    return render_template('manage_applications.html', applications=applications)

@app.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("""SELECT id, message, notification_type, related_id, is_read, created_at 
                 FROM notifications 
                 WHERE user_id = ? 
                 ORDER BY created_at DESC""", (session['user_id'],))
    notifications_raw = c.fetchall()
    
    # Convert datetime strings to datetime objects
    notifications_list = []
    for notif in notifications_raw:
        notif_dict = list(notif)
        # notif[5] is the created_at field
        if notif_dict[5] and isinstance(notif_dict[5], str):
            try:
                notif_dict[5] = datetime.strptime(notif_dict[5], '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                try:
                    notif_dict[5] = datetime.strptime(notif_dict[5], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    notif_dict[5] = None
        notifications_list.append(tuple(notif_dict))
    
    conn.close()
    
    return render_template('notifications.html', notifications=notifications_list)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests"""
    if request.method == 'POST':
        email = sanitize_input(request.form.get('email', '')).lower().strip()
        
        if not email or not validate_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('forgot_password.html')
        
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        c.execute("SELECT id, name FROM users WHERE LOWER(email) = ?", (email,))
        user = c.fetchone()
        conn.close()
        
        if user:
            user_id, name = user
            token = create_reset_token(user_id)
            
            # Send reset email
            reset_url = f"https://start-smart.onrender.com/reset-password/{token}"
            subject = "Password Reset - StartSmart"
            body = f"""Hello {name},

You requested a password reset for your StartSmart account.

Click the link below to reset your password:
{reset_url}

This link will expire in 30 minutes.

If you didn't request this, please ignore this email.

Best regards,
StartSmart Team"""
            
            if send_email(email, subject, body):
                flash('Password reset instructions have been sent to your email.', 'success')
            else:
                flash('Password reset link created. Check your email.', 'info')
        else:
            # Don't reveal if email exists or not for security
            flash('If an account with that email exists, password reset instructions have been sent.', 'info')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token"""
    user_id = validate_reset_token(token)
    
    if not user_id:
        flash('Invalid or expired reset token. Please request a new password reset.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', token=token)
        
        # Update password
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        c.execute("UPDATE users SET password = ? WHERE id = ?", (password_hash, user_id))
        c.execute("UPDATE password_reset_tokens SET used = 1 WHERE token = ?", (token,))
        
        conn.commit()
        conn.close()
        
        flash('Your password has been successfully reset. You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

@app.route('/logout')
def logout():
    """Enhanced logout with user-friendly message"""
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f'You have been successfully logged out. See you soon, {user_name}!', 'info')
    return redirect(url_for('home'))

# ============ MISSING ROUTES FOR TEMPLATE COMPATIBILITY ============

@app.route('/job-map')
def job_map():
    """Interactive job map showing jobs by location"""
    if 'user_id' not in session:
        flash('Please log in to access the job map.')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("""SELECT id, title, company, location, job_type, salary, 
                 created_at, description FROM jobs 
                 WHERE is_active = 1 ORDER BY created_at DESC""")
    jobs = c.fetchall()
    conn.close()
    
    # Group jobs by location for the map
    location_jobs = {}
    for job in jobs:
        location = job[3] if job[3] else 'Unknown Location'
        if location not in location_jobs:
            location_jobs[location] = []
        location_jobs[location].append(job)
    
    return render_template('job_map.html', location_jobs=location_jobs)

@app.route('/mentorship-calendar')
def mentorship_calendar():
    """Calendar view for mentorship sessions"""
    if 'user_id' not in session:
        flash('Please log in to access the mentorship calendar.')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get mentorship sessions for the current user
    if session.get('user_type') == 'mentor':
        c.execute("""SELECT m.*, u.name as mentee_name, u.email as mentee_email
                     FROM mentorship m 
                     JOIN users u ON m.mentee_id = u.id 
                     WHERE m.mentor_id = ? AND m.status = 'accepted'
                     ORDER BY m.created_at DESC""", (session['user_id'],))
    else:
        c.execute("""SELECT m.*, u.name as mentor_name, u.email as mentor_email
                     FROM mentorship m 
                     JOIN users u ON m.mentor_id = u.id 
                     WHERE m.mentee_id = ? AND m.status = 'accepted'
                     ORDER BY m.created_at DESC""", (session['user_id'],))
    
    sessions = c.fetchall()
    conn.close()
    
    return render_template('mentorship_calendar.html', sessions=sessions)

@app.route('/post-job-page')
def post_job_page():
    """Redirect to post_job for consistency"""
    return redirect(url_for('post_job'))

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    """Edit user profile"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    
    if request.method == 'POST':
        name = sanitize_input(request.form.get('name', ''))
        bio = sanitize_input(request.form.get('bio', ''))
        location = sanitize_input(request.form.get('location', ''))
        skills = sanitize_input(request.form.get('skills', ''))
        
        c.execute("UPDATE users SET name = ?, bio = ?, location = ?, skills = ? WHERE id = ?",
                 (name, bio, location, skills, session['user_id']))
        conn.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))
    
    conn.close()
    return render_template('edit_profile.html', user=user)

@app.route('/upload-profile-image', methods=['POST'])
def upload_profile_image():
    """Upload profile image"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'profile_image' not in request.files:
        flash('No file selected!')
        return redirect(url_for('edit_profile'))
    
    file = request.files['profile_image']
    if file.filename == '':
        flash('No file selected!')
        return redirect(url_for('edit_profile'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add user ID to filename to avoid conflicts
        filename = f"profile_{session['user_id']}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(file_path)
            
            # Update user's profile image in database
            conn = sqlite3.connect('startsmart.db')
            c = conn.cursor()
            c.execute("UPDATE users SET profile_image = ? WHERE id = ?", 
                     (filename, session['user_id']))
            conn.commit()
            conn.close()
            
            flash('Profile image uploaded successfully!')
        except Exception as e:
            flash('Failed to upload image. Please try again.')
    else:
        flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF files.')
    
    return redirect(url_for('edit_profile'))

@app.route('/delete-job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    """Delete a job posting"""
    if 'user_id' not in session or session.get('user_type') != 'recruiter':
        flash('Only recruiters can delete jobs!')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Verify the job belongs to the current recruiter
    c.execute("DELETE FROM jobs WHERE id = ? AND posted_by = ?", (job_id, session['user_id']))
    
    if c.rowcount > 0:
        conn.commit()
        flash('Job deleted successfully!')
    else:
        flash('Job not found or you do not have permission to delete it!')
    
    conn.close()
    return redirect(url_for('manage_applications'))

@app.route('/mark-all-read', methods=['GET', 'POST'])
def mark_all_read():
    """Mark all notifications as read"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (session['user_id'],))
    conn.commit()
    conn.close()
    
    flash('All notifications marked as read!')
    return redirect(url_for('notifications'))

# ============ ADDITIONAL ROUTES FOR SRS COMPLIANCE ============

@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if 'user_id' not in session or session.get('user_type') != 'recruiter':
        flash('Only recruiters can post jobs!')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = sanitize_input(request.form.get('title', ''))
        company = sanitize_input(request.form.get('company', ''))
        description = sanitize_input(request.form.get('description', ''))
        location = sanitize_input(request.form.get('location', ''))
        salary = sanitize_input(request.form.get('salary', ''))
        job_type = request.form.get('job_type', '')
        requirements = sanitize_input(request.form.get('requirements', ''))
        benefits = sanitize_input(request.form.get('benefits', ''))
        application_url = sanitize_input(request.form.get('application_url', ''))
        
        if not title or not company or not description or not location or not job_type:
            flash('Please fill in all required fields!')
            return render_template('post_job.html')
        
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        deadline = datetime.now() + timedelta(days=30)  # Default 30 days
        
        c.execute("""INSERT INTO jobs 
                  (title, company, description, location, salary, job_type, posted_by, 
                   created_at, requirements, benefits, deadline, application_url, is_active) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                 (title, company, description, location, salary, job_type, session['user_id'],
                  datetime.now(), requirements, benefits, deadline, application_url, 1))
        
        job_id = c.lastrowid
        conn.commit()
        conn.close()
        
        # Notify all students about the new job
        notify_new_job(title, company)
        
        flash('Job posted successfully!')
        return redirect(url_for('jobs'))
    
    return render_template('post_job.html')

@app.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if 'user_id' not in session or session.get('user_type') != 'recruiter':
        flash('Only recruiters can edit jobs!')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Check if the job belongs to the current recruiter
    c.execute("SELECT * FROM jobs WHERE id = ? AND posted_by = ?", (job_id, session['user_id']))
    job = c.fetchone()
    
    if not job:
        flash('Job not found or you do not have permission to edit it!')
        conn.close()
        return redirect(url_for('manage_applications'))
    
    if request.method == 'POST':
        title = sanitize_input(request.form.get('title', ''))
        company = sanitize_input(request.form.get('company', ''))
        description = sanitize_input(request.form.get('description', ''))
        location = sanitize_input(request.form.get('location', ''))
        salary = sanitize_input(request.form.get('salary', ''))
        job_type = request.form.get('job_type', '')
        requirements = sanitize_input(request.form.get('requirements', ''))
        benefits = sanitize_input(request.form.get('benefits', ''))
        application_url = sanitize_input(request.form.get('application_url', ''))
        is_active = 1 if request.form.get('is_active') == 'on' else 0
        
        c.execute("""UPDATE jobs SET 
                  title = ?, company = ?, description = ?, location = ?, salary = ?, 
                  job_type = ?, requirements = ?, benefits = ?, application_url = ?, is_active = ?
                  WHERE id = ? AND posted_by = ?""",
                 (title, company, description, location, salary, job_type, requirements, 
                  benefits, application_url, is_active, job_id, session['user_id']))
        
        conn.commit()
        conn.close()
        
        flash('Job updated successfully!')
        return redirect(url_for('manage_applications'))
    
    conn.close()
    return render_template('edit_job.html', job=job)

@app.route('/update-application-status', methods=['POST'])
def update_application_status():
    if 'user_id' not in session or session.get('user_type') != 'recruiter':
        return jsonify({'error': 'Unauthorized'}), 403
    
    application_id = request.json.get('application_id')
    new_status = request.json.get('status')
    
    if not application_id or not new_status:
        return jsonify({'error': 'Missing required data'}), 400
    
    if new_status not in ['pending', 'reviewed', 'shortlisted', 'rejected', 'hired']:
        return jsonify({'error': 'Invalid status'}), 400
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Verify the application belongs to a job posted by this recruiter
    c.execute("""SELECT a.id, j.title, u.email, u.name 
                 FROM applications a 
                 JOIN jobs j ON a.job_id = j.id 
                 JOIN users u ON a.user_id = u.id
                 WHERE a.id = ? AND j.posted_by = ?""", 
              (application_id, session['user_id']))
    
    application = c.fetchone()
    
    if not application:
        conn.close()
        return jsonify({'error': 'Application not found'}), 404
    
    # Update the application status
    c.execute("UPDATE applications SET status = ?, updated_at = ? WHERE id = ?",
              (new_status, datetime.now(), application_id))
    
    conn.commit()
    conn.close()
    
    # Send notification to the student
    _, job_title, student_email, student_name = application
    notify_application_status(student_email, job_title, new_status)
    
    return jsonify({'success': True, 'message': 'Application status updated successfully'})

@app.route('/join-startup/<int:startup_id>', methods=['POST'])
def join_startup(startup_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in first'}), 401
    
    if session.get('user_type') not in ['student', 'mentor']:
        return jsonify({'error': 'Only students and mentors can join startups'}), 403
    
    role = sanitize_input(request.json.get('role', ''))
    message = sanitize_input(request.json.get('message', ''))
    
    if not role:
        return jsonify({'error': 'Please specify your role'}), 400
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Check if startup exists
    c.execute("SELECT name, founder_id FROM startups WHERE id = ?", (startup_id,))
    startup = c.fetchone()
    
    if not startup:
        conn.close()
        return jsonify({'error': 'Startup not found'}), 404
    
    # Check if user is already a member
    c.execute("SELECT id FROM startup_members WHERE startup_id = ? AND user_id = ?", 
              (startup_id, session['user_id']))
    
    if c.fetchone():
        conn.close()
        return jsonify({'error': 'You are already a member of this startup'}), 400
    
    # Add user to startup team
    c.execute("INSERT INTO startup_members (startup_id, user_id, role, joined_at) VALUES (?, ?, ?, ?)",
              (startup_id, session['user_id'], role, datetime.now()))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Successfully joined the startup!'})

@app.route('/request-mentorship', methods=['POST'])
def request_mentorship():
    if 'user_id' not in session or session.get('user_type') != 'student':
        return jsonify({'error': 'Only students can request mentorship'}), 403
    
    mentor_id = request.json.get('mentor_id')
    topic = sanitize_input(request.json.get('topic', ''))
    message = sanitize_input(request.json.get('message', ''))
    
    if not mentor_id or not topic or not message:
        return jsonify({'error': 'Please fill in all required fields'}), 400
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Verify mentor exists
    c.execute("SELECT email, name FROM users WHERE id = ? AND user_type = 'mentor'", (mentor_id,))
    mentor = c.fetchone()
    
    if not mentor:
        conn.close()
        return jsonify({'error': 'Mentor not found'}), 404
    
    # Check if there's already a pending request
    c.execute("""SELECT id FROM mentorship 
                 WHERE mentor_id = ? AND mentee_id = ? AND status = 'pending'""", 
              (mentor_id, session['user_id']))
    
    if c.fetchone():
        conn.close()
        return jsonify({'error': 'You already have a pending request with this mentor'}), 400
    
    # Create mentorship request
    c.execute("""INSERT INTO mentorship (mentor_id, mentee_id, topic, message, status, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (mentor_id, session['user_id'], topic, message, 'pending', datetime.now()))
    
    conn.commit()
    conn.close()
    
    # Send email notification to mentor
    mentor_email, mentor_name = mentor
    subject = f"New Mentorship Request: {topic}"
    body = f"Hello {mentor_name},\n\nYou have received a new mentorship request.\n\nTopic: {topic}\nMessage: {message}\n\nLogin to StartSmart to respond."
    send_email(mentor_email, subject, body)
    
    return jsonify({'success': True, 'message': 'Mentorship request sent successfully!'})

@app.route('/respond-mentorship', methods=['POST'])
def respond_mentorship():
    if 'user_id' not in session or session.get('user_type') != 'mentor':
        return jsonify({'error': 'Only mentors can respond to mentorship requests'}), 403
    
    mentorship_id = request.json.get('mentorship_id')
    response = request.json.get('response')  # 'accepted' or 'rejected'
    
    if not mentorship_id or response not in ['accepted', 'rejected']:
        return jsonify({'error': 'Invalid request data'}), 400
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Verify mentorship request belongs to this mentor
    c.execute("""SELECT m.id, m.topic, u.email, u.name 
                 FROM mentorship m 
                 JOIN users u ON m.mentee_id = u.id
                 WHERE m.id = ? AND m.mentor_id = ? AND m.status = 'pending'""", 
              (mentorship_id, session['user_id']))
    
    mentorship = c.fetchone()
    
    if not mentorship:
        conn.close()
        return jsonify({'error': 'Mentorship request not found'}), 404
    
    # Update mentorship status
    c.execute("UPDATE mentorship SET status = ?, updated_at = ? WHERE id = ?",
              (response, datetime.now(), mentorship_id))
    
    conn.commit()
    conn.close()
    
    # Notify student
    _, topic, student_email, student_name = mentorship
    subject = f"Mentorship Request {response.title()}: {topic}"
    body = f"Hello {student_name},\n\nYour mentorship request has been {response}.\n\nTopic: {topic}\n\nLogin to StartSmart for next steps."
    send_email(student_email, subject, body)
    
    return jsonify({'success': True, 'message': f'Mentorship request {response} successfully!'})

@app.route('/mark-notification-read', methods=['POST'])
def mark_notification_read():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    notification_id = request.json.get('notification_id')
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute("UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?",
              (notification_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/mark-all-notifications-read', methods=['POST'])
def mark_all_notifications_read():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (session['user_id'],))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/import-jobs')
def import_jobs():
    """Import jobs from Adzuna API"""
    if 'user_id' not in session or session.get('user_type') not in ['admin', 'recruiter']:
        flash('Only admins and recruiters can import jobs!')
        return redirect(url_for('login'))
    
    try:
        from adzuna_integration import import_jobs_from_adzuna
        count = import_jobs_from_adzuna()
        flash(f'Successfully imported {count} new jobs!', 'success')
    except Exception as e:
        flash(f'Job import failed: {e}', 'error')
    
    return redirect(url_for('jobs'))

@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash('Admin access required!')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get platform statistics
    c.execute("SELECT COUNT(*) FROM users WHERE user_type = 'student'")
    student_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users WHERE user_type = 'mentor'")
    mentor_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users WHERE user_type = 'recruiter'")
    recruiter_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1")
    active_jobs = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM startups")
    startup_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM applications")
    total_applications = c.fetchone()[0]
    
    # Get recent activity
    c.execute("""SELECT 'User Registration' as type, name as title, created_at as date 
                 FROM users 
                 UNION ALL
                 SELECT 'Job Posted' as type, title, created_at 
                 FROM jobs
                 UNION ALL
                 SELECT 'Startup Created' as type, name, created_at 
                 FROM startups
                 ORDER BY date DESC LIMIT 10""")
    recent_activity = c.fetchall()
    
    conn.close()
    
    stats = {
        'students': student_count,
        'mentors': mentor_count,
        'recruiters': recruiter_count,
        'active_jobs': active_jobs,
        'startups': startup_count,
        'applications': total_applications
    }
    
    return render_template('admin.html', stats=stats, recent_activity=recent_activity)

@app.before_request
def check_session_security():
    """Enhanced session security checks"""
    # Skip checks for static files and certain routes
    if request.endpoint in ['static', 'home', 'login', 'register']:
        return
    
    # Check if user session is valid for protected routes
    if 'user_id' in session:
        try:
            # Verify user still exists and is active
            conn = sqlite3.connect('startsmart.db')
            c = conn.cursor()
            c.execute("SELECT id, is_active FROM users WHERE id = ?", (session['user_id'],))
            user = c.fetchone()
            conn.close()
            
            if not user or (len(user) > 1 and not user[1]):
                session.clear()
                flash('Your session has expired. Please log in again.', 'warning')
                return redirect(url_for('login'))
        except:
            # If database check fails, clear session for security
            session.clear()
            return redirect(url_for('login'))

if __name__ == '__main__':
    # Ensure database is properly initialized
    try:
        init_db()
        print("Database initialized successfully")
        
        # Add sample data for production if database is empty
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1")
        job_count = c.fetchone()[0]
        conn.close()
        
        if job_count == 0:
            try:
                from populate_production_data import populate_production_jobs, populate_sample_users
                populate_production_jobs()
                populate_sample_users()
                print("Sample data populated for production")
            except Exception as e:
                print(f"Sample data population failed: {e}")
        
    except Exception as e:
        print(f"Database initialization error: {e}")
        # Try manual database setup
        try:
            from fix_deployment import fix_deployment_database
            fix_deployment_database()
            print("Manual database setup completed")
        except Exception as e2:
            print(f"Manual database setup failed: {e2}")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)