// Admin Panel JavaScript

$(document).ready(function() {
    // Initialize admin panel functionality
    initAdminPanel();
});

function initAdminPanel() {
    // Sidebar toggle for mobile
    $('.sidebar-toggle').on('click', function() {
        $('.sidebar').toggleClass('show');
    });

    // Close sidebar when clicking outside on mobile
    $(document).on('click', function(e) {
        if ($(window).width() <= 768) {
            if (!$(e.target).closest('.sidebar, .sidebar-toggle').length) {
                $('.sidebar').removeClass('show');
            }
        }
    });

    // Set active navigation item
    setActiveNavItem();

    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();

    // Initialize popovers
    $('[data-bs-toggle="popover"]').popover();

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut();
    }, 5000);

    // Initialize data tables
    initDataTables();

    // Initialize form validation
    initFormValidation();

    // Initialize file uploads
    initFileUploads();
}

function setActiveNavItem() {
    const currentPath = window.location.pathname;
    $('.sidebar-nav .nav-link').each(function() {
        const href = $(this).attr('href');
        if (href && currentPath.includes(href.split('/').pop())) {
            $(this).addClass('active');
        }
    });
}

function initDataTables() {
    // Add search functionality to tables
    $('.table').each(function() {
        const table = $(this);
        // Removed dynamic search bar injection
        // const searchInput = $('<input type="text" class="form-control" placeholder="Search..." style="margin-bottom: 10px;">');
        // table.before(searchInput);

        // searchInput.on('keyup', function() {
        //     const value = $(this).val().toLowerCase();
        //     table.find('tbody tr').filter(function() {
        //         $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        //     });
        // });
    });
}

function initFormValidation() {
    // Custom form validation
    $('form').on('submit', function(e) {
        const form = $(this);
        let isValid = true;

        // Clear previous error states
        form.find('.is-invalid').removeClass('is-invalid');
        form.find('.invalid-feedback').remove();

        // Validate required fields
        form.find('[required]').each(function() {
            const field = $(this);
            if (!field.val().trim()) {
                field.addClass('is-invalid');
                field.after('<div class="invalid-feedback">This field is required.</div>');
                isValid = false;
            }
        });

        // Validate email fields
        form.find('input[type="email"]').each(function() {
            const field = $(this);
            const email = field.val();
            if (email && !isValidEmail(email)) {
                field.addClass('is-invalid');
                field.after('<div class="invalid-feedback">Please enter a valid email address.</div>');
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
            showAlert('Please correct the errors in the form.', 'danger');
        }
    });
}

function initFileUploads() {
    // File upload preview
    $('input[type="file"]').on('change', function() {
        const file = this.files[0];
        const preview = $(this).siblings('.file-preview');
        
        if (file && preview.length) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.html(`<img src="${e.target.result}" class="image-preview">`);
                };
                reader.readAsDataURL(file);
            } else {
                preview.html(`<div class="file-info"><i class="fas fa-file"></i> ${file.name}</div>`);
            }
        }
    });
}

// AJAX Functions
function loadData(url, target, params = {}) {
    const loadingHtml = '<div class="text-center"><div class="loading"></div> Loading...</div>';
    $(target).html(loadingHtml);

    $.ajax({
        url: url,
        method: 'GET',
        data: params,
        success: function(response) {
            $(target).html(response);
        },
        error: function(xhr, status, error) {
            $(target).html('<div class="alert alert-danger">Error loading data: ' + error + '</div>');
        }
    });
}

function submitForm(form, successCallback = null) {
    const formData = new FormData(form[0]);
    const submitBtn = form.find('button[type="submit"]');
    const originalText = submitBtn.text();
    
    submitBtn.prop('disabled', true).html('<span class="loading"></span> Saving...');

    $.ajax({
        url: form.attr('action'),
        method: form.attr('method') || 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success) {
                showAlert(response.message || 'Operation completed successfully!', 'success');
                if (successCallback) successCallback(response);
            } else {
                showAlert(response.message || 'Operation failed!', 'danger');
            }
        },
        error: function(xhr, status, error) {
            let errorMessage = 'An error occurred while processing your request.';
            if (xhr.responseJSON && xhr.responseJSON.message) {
                errorMessage = xhr.responseJSON.message;
            }
            showAlert(errorMessage, 'danger');
        },
        complete: function() {
            submitBtn.prop('disabled', false).text(originalText);
        }
    });
}

function deleteItem(url, itemName, btn = null) {
    if (confirm(`Are you sure you want to delete this ${itemName}? This action cannot be undone.`)) {
        $.ajax({
            url: url,
            method: 'POST',
            success: function(response) {
                showAlert(`${itemName} deleted successfully!`, 'success');
                // Remove the row from the table instantly
                if (btn) {
                    $(btn).closest('tr').remove();
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = 'Error deleting item.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                showAlert(errorMessage, 'danger');
            }
        });
    }
}

// Bulk delete function (for projects, etc.)
function bulkDelete(url) {
    const checkedItems = $('.item-checkbox:checked');
    const itemIds = checkedItems.map(function() {
        return $(this).val();
    }).get();
    if (itemIds.length === 0) {
        showAlert('Please select items to delete.', 'warning');
        return;
    }
    if (confirm(`Are you sure you want to delete ${itemIds.length} selected items? This action cannot be undone.`)) {
        $.ajax({
            url: url,
            method: 'POST',
            data: { ids: itemIds },
            success: function(response) {
                showAlert('Selected items deleted successfully!', 'success');
                // Remove all selected rows from the table instantly
                checkedItems.closest('tr').remove();
            },
            error: function(xhr, status, error) {
                let errorMessage = 'Error deleting selected items.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                showAlert(errorMessage, 'danger');
            }
        });
    }
}

// Utility Functions
function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('.content-wrapper').prepend(alertHtml);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut();
    }, 5000);
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function formatCurrency(amount, currency = 'INR') {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN');
}

function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString('en-IN');
}

// Modal Functions
function openModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
}

function closeModal(modalId) {
    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
    if (modal) {
        modal.hide();
    }
}

// Pagination Functions
function loadPage(page, url, target) {
    loadData(url, target, { page: page });
}

// Search and Filter Functions
function applyFilters(form, target) {
    const formData = new FormData(form[0]);
    const params = {};
    
    for (let [key, value] of formData.entries()) {
        if (value) params[key] = value;
    }
    
    loadData(form.attr('action'), target, params);
}

// Export Functions
function exportData(format, url, params = {}) {
    params.format = format;
    const queryString = new URLSearchParams(params).toString();
    window.open(`${url}?${queryString}`, '_blank');
}

// Image Preview Functions
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            $(`#${previewId}`).attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Status Update Functions
function updateStatus(url, status, callback = null) {
    $.ajax({
        url: url,
        method: 'PATCH',
        data: { status: status },
        success: function(response) {
            showAlert('Status updated successfully!', 'success');
            if (callback) callback(response);
        },
        error: function(xhr, status, error) {
            showAlert('Error updating status.', 'danger');
        }
    });
}

// Bulk Operations
function selectAll(checkbox) {
    const isChecked = $(checkbox).is(':checked');
    $('.item-checkbox').prop('checked', isChecked);
    updateBulkActions();
}

function updateBulkActions() {
    const checkedItems = $('.item-checkbox:checked');
    const bulkActions = $('.bulk-actions');
    
    if (checkedItems.length > 0) {
        bulkActions.removeClass('d-none');
        $('.bulk-count').text(checkedItems.length);
    } else {
        bulkActions.addClass('d-none');
    }
}

// Chart Functions (if using charts)
function initCharts() {
    // Initialize any charts if needed
    if (typeof Chart !== 'undefined') {
        // Chart initialization code here
    }
}

// Real-time Updates (if using WebSockets)
function initRealTimeUpdates() {
    // WebSocket connection for real-time updates
    if (typeof io !== 'undefined') {
        const socket = io();
        
        socket.on('data_update', function(data) {
            // Handle real-time data updates
            showAlert('Data has been updated!', 'info');
            // Refresh relevant sections
        });
    }
}

// Keyboard Shortcuts
$(document).on('keydown', function(e) {
    // Ctrl/Cmd + N for new item
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        $('.btn-new').first().click();
    }
    
    // Ctrl/Cmd + S for save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        $('form:visible button[type="submit"]').first().click();
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        $('.modal').modal('hide');
    }
});

// Auto-save functionality
let autoSaveTimer;
function initAutoSave() {
    $('form textarea, form input[type="text"]').on('input', function() {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(function() {
            // Auto-save logic here
            console.log('Auto-saving...');
        }, 2000);
    });
}

// Initialize additional features
$(document).ready(function() {
    initAutoSave();
    initCharts();
    initRealTimeUpdates();
    
    // Update bulk actions when checkboxes change
    $(document).on('change', '.item-checkbox', updateBulkActions);
}); 