from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Input validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text):
    if text is None:
        return ''
    return str(text).strip()[:500]  # Limit length and strip whitespace

def init_db():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, 
                  name TEXT, user_type TEXT, bio TEXT, skills TEXT, location TEXT,
                  resume_file TEXT, created_at TIMESTAMP)''')
    
    # Jobs table
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id INTEGER PRIMARY KEY, title TEXT, company TEXT, description TEXT,
                  location TEXT, salary TEXT, job_type TEXT, posted_by INTEGER, 
                  created_at TIMESTAMP)''')
    
    # Startups table
    c.execute('''CREATE TABLE IF NOT EXISTS startups
                 (id INTEGER PRIMARY KEY, name TEXT, description TEXT, industry TEXT,
                  stage TEXT, founder_id INTEGER, created_at TIMESTAMP)''')
    
    # Applications table
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY, job_id INTEGER, user_id INTEGER, 
                  status TEXT DEFAULT 'pending', applied_at TIMESTAMP,
                  FOREIGN KEY (job_id) REFERENCES jobs (id),
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Mentorship table
    c.execute('''CREATE TABLE IF NOT EXISTS mentorship
                 (id INTEGER PRIMARY KEY, mentor_id INTEGER, mentee_id INTEGER,
                  topic TEXT, status TEXT DEFAULT 'pending', message TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY (mentor_id) REFERENCES users (id),
                  FOREIGN KEY (mentee_id) REFERENCES users (id))''')
    
    # Resources table
    c.execute('''CREATE TABLE IF NOT EXISTS resources
                 (id INTEGER PRIMARY KEY, title TEXT, description TEXT, 
                  category TEXT, file_url TEXT, uploaded_by INTEGER,
                  created_at TIMESTAMP)''')
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = sanitize_input(request.form.get('email', ''))
        password = request.form.get('password', '')
        name = sanitize_input(request.form.get('name', ''))
        user_type = request.form.get('user_type', '')
        
        # Validation
        if not validate_email(email):
            flash('Please enter a valid email address!')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!')
            return render_template('register.html')
        
        if not name or len(name) < 2:
            flash('Please enter a valid name!')
            return render_template('register.html')
        
        if user_type not in ['student', 'mentor', 'recruiter']:
            flash('Please select a valid user type!')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password, name, user_type, created_at) VALUES (?, ?, ?, ?, ?)",
                     (email, password_hash, name, user_type, datetime.now()))
            conn.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!')
        except Exception as e:
            flash('Registration failed. Please try again.')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['user_type'] = user[4]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/jobs')
def jobs():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('job_type', '')
    
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
    
    query += " ORDER BY created_at DESC"
    
    c.execute(query, params)
    jobs = c.fetchall()
    conn.close()
    
    return render_template('jobs.html', jobs=jobs, search=search, location=location, job_type=job_type)

@app.route('/startups')
def startups():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM startups ORDER BY created_at DESC")
    startups = c.fetchall()
    conn.close()
    return render_template('startups.html', startups=startups)

@app.route('/post-job', methods=['POST'])
def post_job():
    if 'user_id' not in session or session['user_type'] != 'recruiter':
        flash('Only recruiters can post jobs!')
        return redirect(url_for('login'))
    
    title = request.form.get('title', '').strip()
    company = request.form.get('company', '').strip()
    description = request.form.get('description', '').strip()
    location = request.form.get('location', '').strip()
    salary = request.form.get('salary', '').strip()
    job_type = request.form.get('job_type', '').strip()
    
    # Validation
    if len(title) < 3:
        flash('Job title must be at least 3 characters long')
        return redirect(url_for('jobs'))
    
    if len(company) < 2:
        flash('Company name must be at least 2 characters long')
        return redirect(url_for('jobs'))
    
    if len(description) < 10:
        flash('Job description must be at least 10 characters long')
        return redirect(url_for('jobs'))
    
    if not location:
        flash('Location is required')
        return redirect(url_for('jobs'))
    
    if not job_type or job_type not in ['full-time', 'part-time', 'internship', 'contract', 'remote', 'hybrid']:
        flash('Please select a valid job type')
        return redirect(url_for('jobs'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO jobs (title, company, description, location, salary, job_type, posted_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                 (title, company, description, location, salary, job_type, session['user_id'], datetime.now()))
        conn.commit()
        flash('Job posted successfully!')
    except Exception as e:
        flash('Failed to post job. Please try again.')
    finally:
        conn.close()
    
    return redirect(url_for('jobs'))

@app.route('/create-startup', methods=['POST'])
def create_startup():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    name = request.form['name']
    description = request.form['description']
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("INSERT INTO startups (name, description, founder_id, created_at) VALUES (?, ?, ?, ?)",
             (name, description, session['user_id'], datetime.now()))
    conn.commit()
    conn.close()
    
    flash('Startup created successfully!')
    return redirect(url_for('startups'))

@app.route('/apply-job/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Check if already applied
    c.execute("SELECT * FROM applications WHERE job_id = ? AND user_id = ?", 
             (job_id, session['user_id']))
    if c.fetchone():
        flash('You have already applied for this job!')
    else:
        c.execute("INSERT INTO applications (job_id, user_id, applied_at) VALUES (?, ?, ?)",
                 (job_id, session['user_id'], datetime.now()))
        conn.commit()
        flash('Application submitted successfully!')
    
    conn.close()
    return redirect(url_for('jobs'))

@app.route('/mentorship')
def mentorship():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_type = 'mentor'")
    mentors = c.fetchall()
    conn.close()
    return render_template('mentorship.html', mentors=mentors)

@app.route('/request-mentorship', methods=['POST'])
def request_mentorship():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    mentor_id = request.form['mentor_id']
    topic = request.form['topic']
    message = request.form['message']
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("INSERT INTO mentorship (mentor_id, mentee_id, topic, message, created_at) VALUES (?, ?, ?, ?, ?)",
             (mentor_id, session['user_id'], topic, message, datetime.now()))
    conn.commit()
    conn.close()
    
    flash('Mentorship request sent successfully!')
    return redirect(url_for('mentorship'))

@app.route('/resources')
def resources():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM resources ORDER BY created_at DESC")
    resources = c.fetchall()
    conn.close()
    return render_template('resources.html', resources=resources)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    
    # Get user's applications
    c.execute("""SELECT j.title, j.company, a.status, a.applied_at 
                 FROM applications a JOIN jobs j ON a.job_id = j.id 
                 WHERE a.user_id = ?""")
    applications = c.fetchall()
    
    conn.close()
    return render_template('profile.html', user=user, applications=applications)

@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash('Admin access required!')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get statistics
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM startups")
    total_startups = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM applications")
    total_applications = c.fetchone()[0]
    
    # Get recent users
    c.execute("SELECT name, email, user_type, created_at FROM users ORDER BY created_at DESC LIMIT 10")
    recent_users = c.fetchall()
    
    # Get recent jobs
    c.execute("SELECT title, company, created_at FROM jobs ORDER BY created_at DESC LIMIT 10")
    recent_jobs = c.fetchall()
    
    conn.close()
    
    stats = {
        'users': total_users,
        'jobs': total_jobs,
        'startups': total_startups,
        'applications': total_applications
    }
    
    return render_template('admin.html', stats=stats, recent_users=recent_users, recent_jobs=recent_jobs)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    
    if not query:
        return jsonify({'results': []})
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    results = []
    
    if category in ['all', 'jobs']:
        c.execute("SELECT 'job' as type, title, company, id FROM jobs WHERE title LIKE ? OR company LIKE ? LIMIT 5",
                 (f"%{query}%", f"%{query}%"))
        jobs = c.fetchall()
        for job in jobs:
            results.append({
                'type': job[0],
                'title': job[1],
                'subtitle': job[2],
                'id': job[3]
            })
    
    if category in ['all', 'startups']:
        c.execute("SELECT 'startup' as type, name, description, id FROM startups WHERE name LIKE ? OR description LIKE ? LIMIT 5",
                 (f"%{query}%", f"%{query}%"))
        startups = c.fetchall()
        for startup in startups:
            results.append({
                'type': startup[0],
                'title': startup[1],
                'subtitle': startup[2][:50] + '...' if len(startup[2]) > 50 else startup[2],
                'id': startup[3]
            })
    
    conn.close()
    return jsonify({'results': results})

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'user_id' not in session:
        return jsonify({'error': 'Login required'}), 401
    
    if 'resume' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.lower().endswith(('.pdf', '.doc', '.docx')):
        filename = secure_filename(f"resume_{session['user_id']}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Update user record with resume filename
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        c.execute("UPDATE users SET resume_file = ? WHERE id = ?", (filename, session['user_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': 'Resume uploaded successfully', 'filename': filename})
    
    return jsonify({'error': 'Invalid file type. Please upload PDF, DOC, or DOCX files only'}), 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)