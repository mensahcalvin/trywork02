// Custom JavaScript for Explore Ghana

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Password strength checker
function checkPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]+/)) strength++;
    if (password.match(/[A-Z]+/)) strength++;
    if (password.match(/[0-9]+/)) strength++;
    if (password.match(/[^a-zA-Z0-9]+/)) strength++;

    return strength;
}

// Image preview for file uploads
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    if (!preview) return;

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button
window.addEventListener('scroll', function() {
    const scrollButton = document.getElementById('scrollToTop');
    if (!scrollButton) return;

    if (window.pageYOffset > 300) {
        scrollButton.style.display = 'block';
    } else {
        scrollButton.style.display = 'none';
    }
});

// Mobile menu toggle
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    if (!menu) return;

    menu.classList.toggle('show');
}

// Form submission handler
function handleFormSubmit(formId, successCallback, errorCallback) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm(formId)) {
            // Here you would typically make an AJAX call
            if (successCallback) successCallback();
        } else {
            if (errorCallback) errorCallback();
        }
    });
}

// Initialize map functionality
function initMap() {
    // This function is called by the Google Maps API
    // Implementation is in the map.html template
}

// Handle transportation type selection
function showTransportDetails(type) {
    const detailsDiv = document.getElementById('transportDetails');
    if (!detailsDiv) return;

    // Implementation is in the transportation.html template
}

// Handle itinerary creation
function createItinerary() {
    const form = document.querySelector('#itineraryForm');
    if (!form) return;

    const formData = new FormData(form);
    const itinerary = {
        name: formData.get('tripName'),
        startDate: formData.get('startDate'),
        endDate: formData.get('endDate'),
        destinations: Array.from(formData.getAll('destinations'))
    };

    // Here you would typically save the itinerary to the backend
    console.log('Creating itinerary:', itinerary);
}

// Add event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Add scroll to top button
    const scrollButton = document.createElement('button');
    scrollButton.id = 'scrollToTop';
    scrollButton.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3';
    scrollButton.innerHTML = '↑';
    scrollButton.onclick = scrollToTop;
    document.body.appendChild(scrollButton);

    // Initialize form handlers
    handleFormSubmit('loginForm', 
        () => console.log('Login successful'),
        () => console.log('Login failed')
    );

    handleFormSubmit('registerForm',
        () => console.log('Registration successful'),
        () => console.log('Registration failed')
    );
}); 