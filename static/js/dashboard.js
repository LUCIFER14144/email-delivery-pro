// Dashboard JavaScript for Email Deliverability Pro

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Show notifications
    function showNotification(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertDiv);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 5000);
    }

    // Loading states for buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                this.innerHTML = `
                    <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                    Processing...
                `;
                this.disabled = true;

                // Re-enable button after 10 seconds as fallback
                setTimeout(() => {
                    this.disabled = false;
                    this.innerHTML = this.getAttribute('data-original-text') || 'Submit';
                }, 10000);
            }
        });

        // Store original text
        button.setAttribute('data-original-text', button.innerHTML);
    });

    // Copy to clipboard functionality
    window.copyToClipboard = function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Copied to clipboard!', 'success');
            }).catch(() => {
                showNotification('Failed to copy to clipboard', 'danger');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                showNotification('Copied to clipboard!', 'success');
            } catch (err) {
                showNotification('Failed to copy to clipboard', 'danger');
            }
            document.body.removeChild(textArea);
        }
    };

    // Character count for subject line
    const subjectInput = document.getElementById('subject');
    if (subjectInput) {
        subjectInput.addEventListener('input', function() {
            const length = this.value.length;
            const helpText = this.nextElementSibling;

            if (helpText && helpText.classList.contains('form-text')) {
                if (length > 50) {
                    helpText.textContent = `${length} characters - Consider shortening for better deliverability`;
                    helpText.className = 'form-text text-warning';
                } else if (length > 40) {
                    helpText.textContent = `${length} characters - Good length`;
                    helpText.className = 'form-text text-info';
                } else {
                    helpText.textContent = `${length} characters - Keep it under 50 for best results`;
                    helpText.className = 'form-text text-muted';
                }
            }
        });
    }

    // Auto-save form data (for spam checker)
    const spamCheckerForm = document.getElementById('spam-checker-form');
    if (spamCheckerForm) {
        const inputs = spamCheckerForm.querySelectorAll('input, textarea');

        // Load saved data
        inputs.forEach(input => {
            const savedValue = localStorage.getItem(`spam_checker_${input.name}`);
            if (savedValue && input.value === '') {
                input.value = savedValue;
            }
        });

        // Save data on input with debounce
        let saveTimeout;
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    localStorage.setItem(`spam_checker_${input.name}`, input.value);
                }, 1000);
            });
        });

        // Clear saved data on successful submit
        spamCheckerForm.addEventListener('submit', () => {
            inputs.forEach(input => {
                localStorage.removeItem(`spam_checker_${input.name}`);
            });
        });
    }

    // Animate progress bars if they exist
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width || bar.getAttribute('aria-valuenow') + '%';
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-in-out';
            bar.style.width = width;
        }, 100);
    });

    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Global utility functions
window.EmailDeliverabilityPro = {
    // Format numbers with commas
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },

    // Calculate time ago
    timeAgo: function(date) {
        const now = new Date();
        const diff = now - new Date(date);
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'Just now';
    },

    // Show loading overlay
    showLoading: function(element) {
        element.classList.add('loading');
        const spinner = document.createElement('div');
        spinner.className = 'spinner-border spinner-border-sm';
        spinner.setAttribute('role', 'status');
        element.appendChild(spinner);
    },

    // Hide loading overlay
    hideLoading: function(element) {
        element.classList.remove('loading');
        const spinner = element.querySelector('.spinner-border');
        if (spinner) spinner.remove();
    }
};
