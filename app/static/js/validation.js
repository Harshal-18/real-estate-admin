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

function validateEmail(email) {
    // Regular expression for basic email validation
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    // Additional checks for common disposable email domains
    const disposableEmailDomains = [
        'tempmail.com', 'throwawaymail.com', 'temp-mail.org', 
        'guerrillamail.com', 'mailinator.com', 'yopmail.com'
    ];

    // Check basic email format
    if (!emailRegex.test(email)) {
        return {
            isValid: false,
            error: 'Please enter a valid email address'
        };
    }

    // Check for disposable email domains
    const domain = email.split('@')[1].toLowerCase();
    if (disposableEmailDomains.includes(domain)) {
        return {
            isValid: false,
            error: 'Please use a valid non-disposable email address'
        };
    }

    return {
        isValid: true,
        error: null
    };
}

function showEmailFeedback(inputId, feedbackId) {
    const emailInput = document.getElementById(inputId);
    const feedbackElement = document.getElementById(feedbackId);
    
    emailInput.addEventListener('input', function() {
        const result = validateEmail(this.value);
        feedbackElement.innerHTML = '';
        feedbackElement.className = 'email-feedback mt-2';
        
        if (this.value.length > 0) {
            if (result.isValid) {
                feedbackElement.innerHTML = '<div class="text-success">Valid email address</div>';
                emailInput.setCustomValidity('');
            } else {
                feedbackElement.innerHTML = `<div class="text-danger">${result.error}</div>`;
                emailInput.setCustomValidity(result.error);
            }
        }
    });

    // Validate on form submission
    emailInput.form.addEventListener('submit', function(e) {
        const result = validateEmail(emailInput.value);
        if (!result.isValid) {
            e.preventDefault();
            feedbackElement.innerHTML = `<div class="text-danger">${result.error}</div>`;
            emailInput.setCustomValidity(result.error);
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
