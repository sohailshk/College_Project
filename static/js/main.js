/**
 * Main JavaScript file for Patient Education Material Generator
 * Handles form submission, file validation, and user interactions
 */

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Patient Education Material Generator loaded');
    
    // Get form elements
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submitBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const alertContainer = document.getElementById('alertContainer');
    
    // Form submission handler
    uploadForm.addEventListener('submit', handleFormSubmit);
    
    // File input change handler
    fileInput.addEventListener('change', handleFileChange);
    
    /**
     * Handle form submission
     * @param {Event} event - Form submit event
     */
    function handleFormSubmit(event) {
        event.preventDefault();
        
        // Validate form inputs
        if (!validateForm()) {
            return;
        }
        
        // Show loading state
        showLoading();
        
        // Create FormData object
        const formData = new FormData(uploadForm);
        
        // Submit form via AJAX
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            handleResponse(data);
        })
        .catch(error => {
            hideLoading();
            console.error('Error:', error);
            showAlert('An error occurred while processing your request. Please try again.', 'danger');
        });
    }
    
    /**
     * Handle file input change
     * @param {Event} event - File change event
     */
    function handleFileChange(event) {
        const file = event.target.files[0];
        
        if (file) {
            // Validate file type
            if (!file.name.toLowerCase().endsWith('.pdf')) {
                showAlert('Please select a PDF file only.', 'warning');
                clearFileInput();
                return;
            }
            
            // Validate file size (16MB max)
            const maxSize = 16 * 1024 * 1024; // 16MB in bytes
            if (file.size > maxSize) {
                showAlert('File size must be less than 16MB.', 'warning');
                clearFileInput();
                return;
            }
            
            // Show file info
            console.log('File selected:', file.name, 'Size:', formatFileSize(file.size));
        }
    }
    
    /**
     * Validate form inputs
     * @returns {boolean} True if form is valid, false otherwise
     */
    function validateForm() {
        const file = fileInput.files[0];
        const educationType = document.getElementById('educationType').value;
        
        // Clear previous alerts
        clearAlerts();
        
        // Check if file is selected
        if (!file) {
            showAlert('Please select a PDF file.', 'warning');
            return false;
        }
        
        // Check if education type is selected
        if (!educationType) {
            showAlert('Please select an education material type.', 'warning');
            return false;
        }
        
        return true;
    }
    
    /**
     * Show loading state
     */
    function showLoading() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        loadingSpinner.style.display = 'block';
        clearAlerts();
    }
    
    /**
     * Hide loading state
     */
    function hideLoading() {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Generate Education Materials';
        loadingSpinner.style.display = 'none';
    }
    
    /**
     * Handle server response
     * @param {Object} data - Response data from server
     */
    function handleResponse(data) {
        if (data.success) {
            showAlert('Education material generated successfully! Redirecting...', 'success');
            
            // Redirect to results page
            setTimeout(() => {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    window.location.href = '/results';
                }
            }, 1500);
            
        } else {
            showAlert(data.error || 'An error occurred. Please try again.', 'danger');
        }
    }
    
    /**
     * Show alert message
     * @param {string} message - Alert message
     * @param {string} type - Alert type (success, danger, warning, info)
     */
    function showAlert(message, type) {
        const alertHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-${getAlertIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        alertContainer.innerHTML = alertHTML;
    }
    
    /**
     * Clear all alert messages
     */
    function clearAlerts() {
        alertContainer.innerHTML = '';
    }
    
    /**
     * Clear file input
     */
    function clearFileInput() {
        fileInput.value = '';
    }
    
    /**
     * Get appropriate icon for alert type
     * @param {string} type - Alert type
     * @returns {string} Font Awesome icon class
     */
    function getAlertIcon(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    /**
     * Format file size for display
     * @param {number} bytes - File size in bytes
     * @returns {string} Formatted file size
     */
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Add drag and drop functionality
    const fileInputArea = fileInput.parentElement;
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileInputArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        fileInputArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        fileInputArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight(e) {
        fileInputArea.classList.add('dragover');
    }
    
    function unhighlight(e) {
        fileInputArea.classList.remove('dragover');
    }
    
    fileInputArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            handleFileChange({ target: { files: files } });
        }
    }
});
