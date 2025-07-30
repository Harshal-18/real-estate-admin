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

function createValidationPopup(inputId) {
    const popup = document.createElement('div');
    popup.className = 'validation-popup';
    popup.innerHTML = `
        <ul>
            <li data-rule="minLength">At least 8 characters</li>
            <li data-rule="hasUpperCase">One uppercase letter</li>
            <li data-rule="hasLowerCase">One lowercase letter</li>
            <li data-rule="hasNumber">One number</li>
            <li data-rule="hasSpecialChar">One special character</li>
        </ul>
    `;
    document.getElementById(inputId).parentElement.appendChild(popup);
    return popup;
}

function showPasswordFeedback(inputId, feedbackId) {
    const passwordInput = document.getElementById(inputId);
    const popup = createValidationPopup(inputId);
    
    function updateValidation() {
        const result = validatePassword(passwordInput.value);
        
        popup.querySelectorAll('li').forEach(li => {
            const rule = li.dataset.rule;
            li.className = result[rule] ? 'valid' : '';
        });

        if (passwordInput.value.length > 0) {
            if (!result.isValid) {
                popup.classList.add('show');
            } else {
                popup.classList.remove('show');
            }
        } else {
            popup.classList.remove('show');
        }
    }

    passwordInput.addEventListener('focus', () => {
        if (!validatePassword(passwordInput.value).isValid) {
            popup.classList.add('show');
        }
    });

    passwordInput.addEventListener('blur', () => {
        setTimeout(() => popup.classList.remove('show'), 200);
    });

    passwordInput.addEventListener('input', updateValidation);
}

function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const disposableEmailDomains = [
        'tempmail.com', 'throwawaymail.com', 'temp-mail.org', 
        'guerrillamail.com', 'mailinator.com', 'yopmail.com'
    ];

    const domain = email.split('@')[1]?.toLowerCase();
    
    return {
        format: emailRegex.test(email),
        validDomain: domain && !disposableEmailDomains.includes(domain),
        isValid: emailRegex.test(email) && domain && !disposableEmailDomains.includes(domain)
    };
}

function showEmailFeedback(inputId, feedbackId) {
    const emailInput = document.getElementById(inputId);
    const popup = document.createElement('div');
    popup.className = 'validation-popup';
    popup.innerHTML = `
        <ul>
            <li data-rule="format">Valid email format (example@domain.com)</li>
            <li data-rule="validDomain">Non-disposable email domain</li>
        </ul>
    `;
    emailInput.parentElement.appendChild(popup);

    function updateValidation() {
        const result = validateEmail(emailInput.value);
        
        popup.querySelectorAll('li').forEach(li => {
            const rule = li.dataset.rule;
            li.className = result[rule] ? 'valid' : '';
        });

        if (emailInput.value.length > 0) {
            if (!result.isValid) {
                popup.classList.add('show');
                emailInput.setCustomValidity('Please enter a valid email address');
            } else {
                popup.classList.remove('show');
                emailInput.setCustomValidity('');
            }
        } else {
            popup.classList.remove('show');
            emailInput.setCustomValidity('');
        }
    }

    emailInput.addEventListener('focus', () => {
        if (!validateEmail(emailInput.value).isValid) {
            popup.classList.add('show');
        }
    });

    emailInput.addEventListener('blur', () => {
        setTimeout(() => popup.classList.remove('show'), 200);
    });

    emailInput.addEventListener('input', updateValidation);

    emailInput.form.addEventListener('submit', function(e) {
        const result = validateEmail(emailInput.value);
        if (!result.isValid) {
            e.preventDefault();
            popup.classList.add('show');
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
