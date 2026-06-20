/**
 * Guards a page by checking if the user is authenticated. If not, redirects to the login page.
 * @returns {void}
 */
function guardPage() {
    if (!getToken()) {
        window.location.href = 'review/login.html';
    }
}

/**
 * Logs the user out by clearing local storage and redirecting to the login page.
 * @returns {void}
 */
function logout() {
    localStorage.clear();
    window.location.href = '/review/login.html';
}

/**
 * Redirects the user to a specific page based on their role.
 * @param {string} role - The role of the user
 * @returns {void}
 */
function redirectByRole(role) {
    const routes = {
        'Pharmacist': '/review/dashboard.html',
        'Cashier': '/review/sales.html',
        'Medical Counter Assistant': '/review/products.html',
        'Rider': '/review/deliveries.html',
        'CEO': '/review/reports.html'
    };

    const page = routes[role] || '/review/dashboard.html';
    window.location.href = page;
}

/**
 * Fetches data from a given URL with specified options, handling authentication and errors.
 * @param {string} url - The URL to fetch data from
 * @param {Object} options - The options for the fetch request
 * @returns {Promise<Response>} - A promise resolving to the fetch response
 */
async function apiFetch(url, options={}) {
    const token = localStorage.getItem('token');
    if (token) {
        options.headers = {
            'Content-Type': 'application/json',
            ...options.headers,
            ...(token && { 'Authorization': `Bearer ${token}` })
        };
    }

    try {
        const response = await fetch(url, options);
        if (response.status === 401) {
            logout();
        }
        return response;
    } catch (error) {
        console.error('Fetch error:', error);
        return null;
    }
}

/**
 * Handles the login process when the user submits the login form.
 * @param {Event} event - The form submission event
 * @returns {Promise<void>}
 */
async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('staffEmail').value.trim();
    const password = document.getElementById('password').value.trim();

    clearError('loginError');

    if (!email || !password) {
        showError('loginError', 'Please enter your email and password.');
        return;
    }

    const response = await apiFetch('http://127.0.0.1:5000/staff/login', {
        method: 'POST',
        //new changes
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ StaffEmail: email, password })
    });

    if (!response) return;

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('staffName', data.staff_name);
        localStorage.setItem('staffRole', data.staff_role);
        localStorage.setItem('staffID', data.staff_id);
        redirectByRole(data.staff_role);
    } else {
        showError('loginError', data.message || 'Login failed. Please try again.');
    }
}

/**
 * Clears the error message from a specified HTML element.
 * @param {string} elementId - The ID of the HTML element to clear
 */
function clearError(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = '';
        //new changes
        element.style.display = 'none';
    }
}

/**
 * Displays an error message in a specified HTML element.
 * @param {string} elementId - The ID of the HTML element to display the error in
 * @param {string} message - The error message to display
 */
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        //new changes
        element.style.display = 'block';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
});

