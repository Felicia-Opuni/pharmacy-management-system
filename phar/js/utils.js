/**
 * Reads the saved token from the browser's localStorage
 * @returns {string|null} The token or null if not found
 */
function getToken() {
    return localStorage.getItem('token');
}

/**
 * Generates authentication headers with the saved token
 * @returns {Object} The headers object
 */
function authHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getToken()
    };
}

/**
 * Fetches data from the API with authentication headers
 * @param {string} url - The API endpoint URL
 * @param {Object} options - The fetch options
 * @returns {Promise<Response>} The API response
 */
async function apiFetch(url, options = {}) {
    options.headers = authHeaders();

    const response = await fetch(url, options);

    if (response.status === 401) {
        localStorage.clear();
        window.location.href = '/review/login.html';
        return;
    }

    return response;
}


/**
 * Formats an ID with a given prefix, number, and padding
 * @param {string} prefix - The prefix for the ID
 * @param {number} number - The number to format
 * @param {number} padding - The number of digits to pad
 * @returns {string} The formatted ID
*/
function formatID(prefix, number, padding) {
    return prefix + String(number).padStart(padding, '0');
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-GB', {
        day: 'numeric', month: 'long', year: 'numeric'
    });
}

function formatCurrency(amount) {
    return 'GHS ' + parseFloat(amount).toFixed(2);
}
 

/***
 * Displays an error message in a specified HTML element
 * @param {string} elementId - The ID of the HTML element
 * @param {string} message - The error message to display
   */
function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = message;
        el.style.display = 'block';
    }
}

function clearError(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = '';
        el.style.display = 'none';
    }
}

/**
 * Prompts the user for confirmation before deleting a record
 * @param {string} message - The confirmation message
 * @returns {boolean} True if the user confirms, false otherwise
*/
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this record?');
}

/**
 * Sets the active navigation link based on the current page URL
 */
function setActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav-item');

    navLinks.forEach(function(link) {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
}

/**
 * Sets the date in the header based on the current date
 */
function setHeaderDate() {
    const dateEl = document.querySelector('.header-date');
    if (dateEl) {
        const today = new Date();
        dateEl.textContent = '📅 ' + today.toLocaleDateString('en-GB', {
            weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
        });
    }
}

/**
 * Sets the user information in the sidebar based on the saved data
 */
function setSidebarUser() {
    const nameEl = document.querySelector('.user-name');
    const roleEl = document.querySelector('.user-role');
    const avatarEl = document.querySelector('.user-avatar');

    const name = localStorage.getItem('staffName');
    const role = localStorage.getItem('staffRole');

    if (nameEl && name) nameEl.textContent = name;
    if (roleEl && role) roleEl.textContent = role;
    if (avatarEl && name) {
        const parts = name.split(' ');
        avatarEl.textContent = parts[0][0] + (parts[1] ? parts[1][0] : '');
    }
}

/**
 * Initializes the page by setting active navigation link, header date, and sidebar user information
 */
document.addEventListener('DOMContentLoaded', function() {
    setActiveNavLink();
    setHeaderDate();
    setSidebarUser();
});