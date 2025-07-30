/**
 * StartSmart Job Posting
 * JavaScript functionality for job posting and application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Job posting form validation
    const jobPostingForm = document.getElementById('job-posting-form');
    
    if (jobPostingForm) {
        jobPostingForm.addEventListener('submit', function(e) {
            const title = document.getElementById('title').value.trim();
            const company = document.getElementById('company').value.trim();
            const description = document.getElementById('description').value.trim();
            const location = document.getElementById('location').value.trim();
            const jobType = document.getElementById('job_type').value;
            const requirements = document.getElementById('requirements').value.trim();
            const applicationUrl = document.getElementById('application_url').value.trim();
            
            let isValid = true;
            let errorMessages = [];
            
            // Clear previous error messages
            document.querySelectorAll('.is-invalid').forEach(el => {
                el.classList.remove('is-invalid');
            });
            
            // Validate title
            if (title.length < 3) {
                document.getElementById('title').classList.add('is-invalid');
                errorMessages.push('Job title must be at least 3 characters long');
                isValid = false;
            }
            
            // Validate company
            if (company.length < 2) {
                document.getElementById('company').classList.add('is-invalid');
                errorMessages.push('Company name must be at least 2 characters long');
                isValid = false;
            }
            
            // Validate description
            if (description.length < 10) {
                document.getElementById('description').classList.add('is-invalid');
                errorMessages.push('Job description must be at least 10 characters long');
                isValid = false;
            }
            
            // Validate location
            if (!location) {
                document.getElementById('location').classList.add('is-invalid');
                errorMessages.push('Location is required');
                isValid = false;
            }
            
            // Validate job type
            if (!jobType) {
                document.getElementById('job_type').classList.add('is-invalid');
                errorMessages.push('Job type is required');
                isValid = false;
            }
            
            // Validate requirements
            if (requirements.length < 10) {
                document.getElementById('requirements').classList.add('is-invalid');
                errorMessages.push('Requirements must be at least 10 characters long');
                isValid = false;
            }
            
            // Validate application URL
            if (!applicationUrl || (!applicationUrl.startsWith('http://') && !applicationUrl.startsWith('https://'))) {
                document.getElementById('application_url').classList.add('is-invalid');
                errorMessages.push('Please provide a valid application URL starting with http:// or https://');
                isValid = false;
            }
            
            // Show error messages
            if (!isValid) {
                e.preventDefault();
                
                // Display error messages
                const errorContainer = document.getElementById('error-container');
                if (errorContainer) {
                    errorContainer.innerHTML = '';
                    errorMessages.forEach(message => {
                        const alert = document.createElement('div');
                        alert.className = 'alert alert-danger';
                        alert.textContent = message;
                        errorContainer.appendChild(alert);
                    });
                    
                    // Scroll to error container
                    errorContainer.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    }
    
    // Job application form validation
    const jobApplicationForm = document.getElementById('job-application-form');
    
    if (jobApplicationForm) {
        jobApplicationForm.addEventListener('submit', function(e) {
            const coverLetter = document.getElementById('cover_letter');
            
            if (coverLetter && coverLetter.value.trim().length < 50) {
                e.preventDefault();
                coverLetter.classList.add('is-invalid');
                
                // Show error message
                const errorMessage = document.createElement('div');
                errorMessage.className = 'invalid-feedback';
                errorMessage.textContent = 'Cover letter should be at least 50 characters long';
                
                // Remove any existing error message
                const existingError = coverLetter.nextElementSibling;
                if (existingError && existingError.className === 'invalid-feedback') {
                    existingError.remove();
                }
                
                coverLetter.parentNode.appendChild(errorMessage);
            }
        });
    }
    
    // Job filter functionality
    const jobFilters = document.getElementById('job-filters');
    
    if (jobFilters) {
        const filterForm = jobFilters.querySelector('form');
        const filterInputs = jobFilters.querySelectorAll('input, select');
        
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }
    
    // Job search functionality
    const jobSearch = document.getElementById('job-search');
    
    if (jobSearch) {
        const searchInput = jobSearch.querySelector('input[type="search"]');
        const searchButton = jobSearch.querySelector('button[type="submit"]');
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchButton.click();
            }
        });
    }
});