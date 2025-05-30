from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/jobs')
def jobs():
    job_listings = [
        {"title": "Frontend Developer Intern", "company": "Tech4Africa", "location": "Remote"},
        {"title": "Startup Marketing Assistant", "company": "Green Growth Hub", "location": "Kigali"},
        {"title": "Junior Data Analyst", "company": "Youth Insights", "location": "Nairobi"}
    ]
    return render_template('jobs.html', jobs=job_listings)

@bp.route('/mentorship')
def mentorship():
    mentors = [
        {"name": "Amina Yusuf", "field": "Software Engineering", "location": "Lagos"},
        {"name": "John Kamau", "field": "Product Design", "location": "Nairobi"},
        {"name": "Grace Mbabazi", "field": "Startup Strategy", "location": "Kigali"}
    ]
    return render_template('mentorship.html', mentors=mentors)

@bp.route('/startups')
def startups():
    featured_startups = [
        {"name": "AgriSmart", "industry": "AgriTech", "location": "Kigali"},
        {"name": "EcoBuild", "industry": "Green Construction", "location": "Nairobi"},
        {"name": "Finlite", "industry": "FinTech", "location": "Lagos"}
    ]
    return render_template('startups.html', startups=featured_startups)
