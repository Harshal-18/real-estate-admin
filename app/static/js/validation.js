function validatePassword(password) {
    const minLength = 8;
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);

    let errors = [];
    if (password.length < minLength) {
        errors.push('Password must be at least 8 characters long');
    }
    if (!hasNumber) {
        errors.push('Password must contain at least one number');
    }
    if (!hasSpecialChar) {
        errors.push('Password must contain at least one special character');
    }
    if (!hasUpperCase) {
        errors.push('Password must contain at least one uppercase letter');
    }
    if (!hasLowerCase) {
        errors.push('Password must contain at least one lowercase letter');
    }

    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

function showPasswordFeedback(inputId, feedbackId) {
    const passwordInput = document.getElementById(inputId);
    const feedbackElement = document.getElementById(feedbackId);
    
    passwordInput.addEventListener('input', function() {
        const result = validatePassword(this.value);
        feedbackElement.innerHTML = '';
        feedbackElement.className = 'password-feedback mt-2';
        
        if (this.value.length > 0) {
            if (result.isValid) {
                feedbackElement.innerHTML = '<div class="text-success">Password meets all requirements</div>';
            } else {
                const errorList = result.errors.map(error => `<li>${error}</li>`).join('');
                feedbackElement.innerHTML = `<ul class="text-danger mb-0">${errorList}</ul>`;
            }
        }
    });
}

function validatePasswordMatch(passwordId, confirmPasswordId, feedbackId) {
    const passwordInput = document.getElementById(passwordId);
    const confirmPasswordInput = document.getElementById(confirmPasswordId);
    const feedbackElement = document.getElementById(feedbackId);

    function checkMatch() {
        if (confirmPasswordInput.value.length > 0) {
            if (passwordInput.value === confirmPasswordInput.value) {
                feedbackElement.innerHTML = '<div class="text-success">Passwords match</div>';
            } else {
                feedbackElement.innerHTML = '<div class="text-danger">Passwords do not match</div>';
            }
        } else {
            feedbackElement.innerHTML = '';
        }
    }

    confirmPasswordInput.addEventListener('input', checkMatch);
    passwordInput.addEventListener('input', checkMatch);
}
