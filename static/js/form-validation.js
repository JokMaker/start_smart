/**
 * Production-Ready Form Validation
 * Enhanced client-side validation for better user experience
 */

class FormValidator {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.errors = new Map();
        this.init();
    }
    
    init() {
        if (!this.form) return;
        
        // Add real-time validation
        const inputs = this.form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
        
        // Enhanced form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }
    
    validateField(field) {
        const value = field.value.trim();
        const name = field.name;
        let isValid = true;
        let errorMessage = '';
        
        // Clear previous errors
        this.clearFieldError(field);
        
        switch(name) {
            case 'name':
                if (!value) {
                    errorMessage = 'Full name is required';
                    isValid = false;
                } else if (value.length < 2) {
                    errorMessage = 'Name must be at least 2 characters';
                    isValid = false;
                } else if (value.length > 100) {
                    errorMessage = 'Name must be less than 100 characters';
                    isValid = false;
                } else if (!/^[a-zA-Z\s\'-\.]+$/.test(value)) {
                    errorMessage = 'Name can only contain letters, spaces, hyphens, and periods';
                    isValid = false;
                }
                break;
                
            case 'email':
                const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                if (!value) {
                    errorMessage = 'Email address is required';
                    isValid = false;
                } else if (!emailRegex.test(value)) {
                    errorMessage = 'Please enter a valid email address';
                    isValid = false;
                } else if (value.length > 254) {
                    errorMessage = 'Email address is too long';
                    isValid = false;
                }
                break;
                
            case 'password':
                if (!value) {
                    errorMessage = 'Password is required';
                    isValid = false;
                } else {
                    const passwordErrors = this.validatePassword(value);
                    if (passwordErrors.length > 0) {
                        errorMessage = passwordErrors[0];
                        isValid = false;
                    }
                }
                break;
                
            case 'confirmPassword':
                const password = this.form.querySelector('[name="password"]').value;
                if (!value) {
                    errorMessage = 'Please confirm your password';
                    isValid = false;
                } else if (value !== password) {
                    errorMessage = 'Passwords do not match';
                    isValid = false;
                }
                break;
                
            case 'user_type':
                if (!value) {
                    errorMessage = 'Please select your role';
                    isValid = false;
                }
                break;
        }
        
        if (!isValid) {
            this.showFieldError(field, errorMessage);
            this.errors.set(name, errorMessage);
        } else {
            this.showFieldSuccess(field);
            this.errors.delete(name);
        }
        
        return isValid;
    }
    
    validatePassword(password) {
        const errors = [];
        
        if (password.length < 8) {
            errors.push('Password must be at least 8 characters long');
        }
        if (password.length > 128) {
            errors.push('Password must be less than 128 characters');
        }
        if (!/[a-z]/.test(password)) {
            errors.push('Password must contain at least one lowercase letter');
        }
        if (!/[A-Z]/.test(password)) {
            errors.push('Password must contain at least one uppercase letter');
        }
        if (!/\d/.test(password)) {
            errors.push('Password must contain at least one number');
        }
        if (!/[@$!%*?&#^()_+=\-\[\]{}|\\:;"'<>,.?/~`]/.test(password)) {
            errors.push('Password must contain at least one special character');
        }
        
        return errors;
    }
    
    showFieldError(field, message) {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        
        // Show error message
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    }
    
    showFieldSuccess(field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        
        // Hide error message
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    }
    
    clearFieldError(field) {
        field.classList.remove('is-invalid', 'is-valid');
        
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    }
    
    handleSubmit(e) {
        // Validate all fields
        const inputs = this.form.querySelectorAll('input[required], select[required]');
        let allValid = true;
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                allValid = false;
            }
        });

        if (!allValid) {
            e.preventDefault();
            e.stopPropagation();
            
            // Show error summary
            this.showErrorSummary();
            return false;
        }
        
        // Show loading state
        this.showLoadingState();
        return true;
    }
    
    showErrorSummary() {
        // Focus on first error field
        const firstError = this.form.querySelector('.is-invalid');
        if (firstError) {
            firstError.focus();
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        
        // Show toast notification
        this.showToast('Please correct the errors below and try again.', 'error');
    }
    
    showLoadingState() {
        const submitBtn = this.form.querySelector('[type="submit"]');
        if (submitBtn) {
            const btnText = submitBtn.querySelector('.btn-text');
            const btnLoading = submitBtn.querySelector('.btn-loading');
            
            if (btnText && btnLoading) {
                btnText.classList.add('d-none');
                btnLoading.classList.remove('d-none');
                submitBtn.disabled = true;
            }
        }
    }
    
    showToast(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
        toast.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }
}

// Password strength indicator
class PasswordStrengthIndicator {
    constructor(passwordFieldId, indicatorId) {
        this.passwordField = document.getElementById(passwordFieldId);
        this.indicator = document.getElementById(indicatorId);
        this.init();
    }
    
    init() {
        if (!this.passwordField || !this.indicator) return;
        
        this.passwordField.addEventListener('input', () => {
            this.updateStrength();
        });
    }
    
    updateStrength() {
        const password = this.passwordField.value;
        const strength = this.calculateStrength(password);
        
        this.indicator.className = `password-strength ${strength.class}`;
        this.indicator.textContent = strength.text;
        
        // Update progress bar if exists
        const progressBar = this.indicator.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = strength.percentage + '%';
        }
    }
    
    calculateStrength(password) {
        if (!password) {
            return { class: '', text: '', percentage: 0 };
        }
        
        let score = 0;
        const checks = {
            length: password.length >= 8,
            lowercase: /[a-z]/.test(password),
            uppercase: /[A-Z]/.test(password),
            number: /\d/.test(password),
            special: /[@$!%*?&#^()_+=\-\[\]{}|\\:;"'<>,.?/~`]/.test(password)
        };
        
        score = Object.values(checks).filter(Boolean).length;
        
        if (score <= 2) {
            return { class: 'weak', text: 'Weak', percentage: 25 };
        } else if (score === 3) {
            return { class: 'fair', text: 'Fair', percentage: 50 };
        } else if (score === 4) {
            return { class: 'good', text: 'Good', percentage: 75 };
        } else {
            return { class: 'strong', text: 'Strong', percentage: 100 };
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation
    if (document.getElementById('registerForm')) {
        new FormValidator('registerForm');
        new PasswordStrengthIndicator('password', 'passwordStrength');
    }
    
    if (document.getElementById('loginForm')) {
        new FormValidator('loginForm');
    }
    
    // Auto-hide flash messages
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 5000);
    });
});
