document.addEventListener('DOMContentLoaded', function() {
    // Save job functionality
    const saveButtons = document.querySelectorAll('.save-job');
    saveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const jobId = this.getAttribute('data-job-id');
            
            // Toggle saved state
            if (this.classList.contains('saved')) {
                this.classList.remove('saved');
                this.classList.remove('btn-primary');
                this.classList.add('btn-outline-secondary');
                this.innerHTML = '<i class="far fa-bookmark me-2"></i>Save Job';
                
                // Show toast notification
                showToast('Job removed from saved items', 'info');
            } else {
                this.classList.add('saved');
                this.classList.remove('btn-outline-secondary');
                this.classList.add('btn-primary');
                this.innerHTML = '<i class="fas fa-bookmark me-2"></i>Saved';
                
                // Show toast notification
                showToast('Job saved successfully!', 'success');
            }
        });
    });
    
    // Filter functionality
    const filterCheckboxes = document.querySelectorAll('.form-check-input');
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            // Get the current URL and parameters
            const url = new URL(window.location.href);
            const params = new URLSearchParams(url.search);
            
            // Update or remove the job_type parameter based on checkbox state
            if (this.checked) {
                params.set('job_type', this.value);
            } else {
                params.delete('job_type');
            }
            
            // Redirect to the updated URL
            window.location.href = `${url.pathname}?${params.toString()}`;
        });
    });
    
    // Ensure only one job type checkbox is checked at a time
    document.querySelectorAll('input[name="job_type"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                document.querySelectorAll('input[name="job_type"]').forEach(cb => {
                    if (cb !== this) cb.checked = false;
                });
            }
        });
    });
    
    // Sort functionality
    const sortSelect = document.querySelector('.form-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            // In a real application, this would trigger a form submission or AJAX request
            // For demo purposes, we'll just show a toast notification
            showToast(`Jobs sorted by ${this.value}`, 'info');
        });
    }
    
    // Toast notification function
    function showToast(message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container');
        
        if (!toastContainer) return;
        
        const toast = document.createElement('div');
        toast.className = `toast show toast-${type}`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        const icon = type === 'success' ? 'check-circle' : 
                    type === 'warning' ? 'exclamation-triangle' : 
                    type === 'danger' ? 'exclamation-circle' : 'info-circle';
        
        toast.innerHTML = `
            <div class="toast-header">
                <i class="fas fa-${icon} me-2"></i>
                <strong class="me-auto">StartSmart</strong>
                <small>Just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        // Auto-remove toast after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 5000);
        
        // Add click event to close button
        const closeButton = toast.querySelector('.btn-close');
        closeButton.addEventListener('click', function() {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 300);
        });
    }
});