// EMERGENCY OVERRIDE - Disable all password validation
console.log("🚨 EMERGENCY: Password validation disabled for testing");

// Override validatePassword function globally
window.validatePassword = function(password) {
    if (password.length < 3) {
        return ['Password too short'];
    }
    return []; // No validation errors
};

// Override form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            console.log('Form submitted - validation bypassed');
        });
    });
});

// Disable any existing validation
setTimeout(function() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.removeAttribute('pattern');
        input.removeAttribute('required');
    });
    console.log('Password requirements removed');
}, 100);
