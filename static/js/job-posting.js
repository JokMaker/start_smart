// Job posting form validation and guidance
document.addEventListener('DOMContentLoaded', function() {
    const jobForm = document.querySelector('#postJobModal form');
    const titleInput = document.querySelector('input[name="title"]');
    const companyInput = document.querySelector('input[name="company"]');
    const descriptionInput = document.querySelector('textarea[name="description"]');
    const locationInput = document.querySelector('input[name="location"]');
    const jobTypeSelect = document.querySelector('select[name="job_type"]');
    
    if (!jobForm) return;
    
    // Real-time validation feedback
    function validateField(field, minLength, fieldName) {
        const value = field.value.trim();
        const isValid = value.length >= minLength;
        
        field.classList.toggle('is-valid', isValid && value.length > 0);
        field.classList.toggle('is-invalid', !isValid && value.length > 0);
        
        return isValid;
    }
    
    // Add event listeners for real-time validation
    titleInput?.addEventListener('input', function() {
        validateField(this, 3, 'Title');
        updateCharCount(this, 'title-count', 3);
    });
    
    companyInput?.addEventListener('input', function() {
        validateField(this, 2, 'Company');
    });
    
    descriptionInput?.addEventListener('input', function() {
        validateField(this, 10, 'Description');
        updateCharCount(this, 'desc-count', 10);
    });
    
    locationInput?.addEventListener('input', function() {
        validateField(this, 1, 'Location');
    });
    
    // Form submission validation
    jobForm.addEventListener('submit', function(e) {
        let isValid = true;
        const errors = [];
        
        if (!validateField(titleInput, 3)) {
            errors.push('Job title must be at least 3 characters');
            isValid = false;
        }
        
        if (!validateField(companyInput, 2)) {
            errors.push('Company name must be at least 2 characters');
            isValid = false;
        }
        
        if (!validateField(descriptionInput, 10)) {
            errors.push('Description must be at least 10 characters');
            isValid = false;
        }
        
        if (!locationInput.value.trim()) {
            errors.push('Location is required');
            isValid = false;
        }
        
        if (!jobTypeSelect.value || !['full-time', 'part-time', 'internship', 'contract', 'remote', 'hybrid'].includes(jobTypeSelect.value)) {
            errors.push('Please select a valid job type');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
            showValidationErrors(errors);
        }
    });
    
    function updateCharCount(field, countId, minLength) {
        const count = field.value.length;
        const remaining = Math.max(0, minLength - count);
        const color = count >= minLength ? 'text-success' : 'text-warning';
        
        // You can add character count display here if needed
    }
    
    function showValidationErrors(errors) {
        const errorHtml = errors.map(error => `<li>${error}</li>`).join('');
        const alertHtml = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <strong>Please fix the following errors:</strong>
                <ul class="mb-0 mt-2">${errorHtml}</ul>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const modalBody = document.querySelector('#postJobModal .modal-body');
        const existingAlert = modalBody.querySelector('.alert-danger');
        if (existingAlert) {
            existingAlert.remove();
        }
        
        modalBody.insertAdjacentHTML('afterbegin', alertHtml);
    }
});