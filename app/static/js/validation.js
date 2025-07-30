function validatePassword(password) {
    return {
        minLength: password.length >= 8,
        hasNumber: /\d/.test(password),
        hasSpecialChar: /[!@#$%^&*(),.?":{}|<>]/.test(password),
        hasUpperCase: /[A-Z]/.test(password),
        hasLowerCase: /[a-z]/.test(password),
        isValid: password.length >= 8 && 
                /\d/.test(password) && 
                /[!@#$%^&*(),.?":{}|<>]/.test(password) && 
                /[A-Z]/.test(password) && 
                /[a-z]/.test(password)
    };
}

function showPasswordFeedback(inputId, feedbackId) {
    const passwordInput = document.getElementById(inputId);
    const feedbackElement = document.getElementById(feedbackId);
    feedbackElement.className = 'validation-feedback';
    
    // Create rules list
    const rulesList = document.createElement('ul');
    rulesList.style.display = 'none';
    rulesList.innerHTML = `
        <li data-rule="minLength">At least 8 characters long</li>
        <li data-rule="hasUpperCase">One uppercase letter</li>
        <li data-rule="hasLowerCase">One lowercase letter</li>
        <li data-rule="hasNumber">One number</li>
        <li data-rule="hasSpecialChar">One special character</li>
    `;
    feedbackElement.appendChild(rulesList);
    
    function updateValidation() {
        const result = validatePassword(passwordInput.value);
        
        if (passwordInput.value.length > 0) {
            rulesList.style.display = 'block';
            rulesList.querySelectorAll('li').forEach(li => {
                const rule = li.dataset.rule;
                li.className = result[rule] ? 'valid' : '';
            });
        } else {
            rulesList.style.display = 'none';
        }
    }

    // Show validation on blur if password is invalid
    passwordInput.addEventListener('blur', () => {
        const result = validatePassword(passwordInput.value);
        if (passwordInput.value.length > 0 && !result.isValid) {
            rulesList.style.display = 'block';
            updateValidation();
        }
    });

    passwordInput.addEventListener('input', updateValidation);
}

function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const disposableEmailDomains = [
        'tempmail.com', 'throwawaymail.com', 'temp-mail.org', 
        'guerrillamail.com', 'mailinator.com', 'yopmail.com'
    ];

    if (!email.includes('@')) {
        return {
            error: 'Email must contain @ symbol',
            isValid: false
        };
    }

    if (!email.includes('.')) {
        return {
            error: 'Email must contain a domain (e.g., .com, .org)',
            isValid: false
        };
    }

    if (!emailRegex.test(email)) {
        return {
            error: 'Please enter a valid email format (example@domain.com)',
            isValid: false
        };
    }

    const domain = email.split('@')[1].toLowerCase();
    if (disposableEmailDomains.includes(domain)) {
        return {
            error: 'Please use a valid non-disposable email address',
            isValid: false
        };
    }

    return {
        isValid: true
    };
}

function showEmailFeedback(inputId, feedbackId) {
    const emailInput = document.getElementById(inputId);
    const feedbackElement = document.getElementById(feedbackId);
    feedbackElement.className = 'validation-feedback';

    function updateValidation() {
        const result = validateEmail(emailInput.value);
        
        if (emailInput.value.length > 0) {
            if (!result.isValid) {
                feedbackElement.innerHTML = `<div class="error-message">${result.error}</div>`;
                emailInput.setCustomValidity(result.error);
            } else {
                feedbackElement.innerHTML = '<div class="success-message">Valid email address</div>';
                emailInput.setCustomValidity('');
            }
        } else {
            feedbackElement.innerHTML = '';
            emailInput.setCustomValidity('');
        }
    }

    // Show validation on blur
    emailInput.addEventListener('blur', () => {
        if (emailInput.value.length > 0) {
            updateValidation();
        }
    });

    emailInput.addEventListener('input', updateValidation);

    emailInput.form.addEventListener('submit', function(e) {
        const result = validateEmail(emailInput.value);
        if (!result.isValid) {
            e.preventDefault();
            updateValidation();
            emailInput.focus();
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
