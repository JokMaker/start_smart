from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.job_service import get_all_jobs, create_job  # Example service functions
from app.models.job import Job

# Create a Blueprint for job-related routes
jobs = Blueprint('jobs', __name__)

@jobs.route('/jobs')
def job_listings():
    """Display a list of all jobs."""
    jobs = get_all_jobs()  # Fetch jobs from the database via the service layer
    return render_template('jobs.html', jobs=jobs)

@jobs.route('/jobs/create', methods=['GET', 'POST'])
def create_job_route():
    """Create a new job listing."""
    if request.method == 'POST':
        title = request.form.get('title')
        company = request.form.get('company')
        location = request.form.get('location')
        description = request.form.get('description')

        # Call the service function to create the job
        create_job(title=title, company=company, location=location, description=description)
        flash('Job created successfully!', 'success')
        return redirect(url_for('jobs.job_listings'))

    return render_template('create_job.html')  # Template for creating a job