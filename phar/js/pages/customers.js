guardPage()

//An array to hold all customers for
//to make the search and filtter functions work without making multiple API calls.
let allCustomers=[]
let currentCustomersPage = 1;
const rowsPerPage = 10;

//This function fetches all products from Flask and builds the table:
async function loadCustomers(){
    const response = await apiFetch('http://127.0.0.1:5000/customer');
    if (!response) return;

    const data = await response.json();
    allCustomers = data;
    renderCustomerTable(allCustomers);
}

function getHealthBadge(status) {
    const badges = {
        'Healthy': 'badge-green',
        'Diabetic': 'badge-orange',
        'Hypertensive': 'badge-amber',
        'Pregnant': 'badge-blue',
        'Asthmatic': 'badge-grey'
    };
    const badgeClass = badges[status] || 'badge-grey';
    return `<span class="badge ${badgeClass}">${status}</span>`;
}

//This function takes a list of customers and builds the table rows:
function renderCustomerTable(customers){
    const tbody = document.getElementById('customersTableBody');
    tbody.innerHTML = '';
    document.getElementById('customerCount').textContent = 
    'Showing ' + customers.length + ' customer' + (customers.length !== 1 ? 's' : '') + ' registered';
    

    if (customers.length ===0 ){
        tbody.innerHTML = '<tr><td colspan="9" class="text-center td-muted">No customers found.</td></tr>';
        return;
    }

    const start = (currentCustomersPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const pageRows = customers.slice(start, end);

    pageRows.forEach(function(customer) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="td-id">${formatID('C', customer.CustomerID, 3)}</td>
            <td class="td-bold">${customer.CustomerFName} ${customer.CustomerSName}</td>
            <td class="td-muted">${customer.CustomerGender}</td>
            <td>${formatDate(customer.DateOfBirth)}</td>
            <td>${customer.CustomerPhoneNumber}</td>
            <td>${getHealthBadge(customer.CustomerHealthStatus)}</td>
            <td>
                <a href="health_records.html" class="btn btn-icon btn-sm" title="Health Records">🩺</a>
                <button class="btn btn-icon btn-sm" title="Edit" onclick="openEditModal(${customer.CustomerID})">✏️</button>
                <button class="btn btn-icon btn-sm" onclick="deleteCustomer(${customer.CustomerID})">🗑️</button>
            </td>
        `;
        tbody.appendChild(row);
        
    });
    renderCustomersPagination(customers);
}

function renderCustomersPagination(customers) {
    const pagination = document.getElementById('customersPagination');
    pagination.innerHTML = '';

    const totalPages = Math.ceil(customers.length / rowsPerPage);

    if (totalPages <= 1) {
        pagination.style.display = 'none';
        return;
    }

    pagination.style.display = 'flex';

    const prevBtn = document.createElement('button');
    prevBtn.className = 'page-btn' + (currentCustomerPage === 1 ? ' disabled' : '');
    prevBtn.textContent = '‹';
    prevBtn.onclick = function() {
        if (currentCustomersPage > 1) {
            currentCustomersPage--;
            renderCustomersTable(getFilteredCustomers());
        }
    };
    pagination.appendChild(prevBtn);

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.className = 'page-btn' + (i === currentCustomersPage ? ' active' : '');
        btn.textContent = i;
        btn.onclick = function() {
            currentCustomersPage = i;
            renderCustomersTable(getFilteredCustomers());
        };
        pagination.appendChild(btn);
    }

    const nextBtn = document.createElement('button');
    nextBtn.className = 'page-btn' + (currentCustomerPage === totalPages ? ' disabled' : '');
    nextBtn.textContent = '›';
    nextBtn.onclick = function() {
        if (currenCustomersPage < totalPages) {
            currentCustomersPage++;
            renderCustomersTable(getFilteredCustomers());
        }
    };
    pagination.appendChild(nextBtn);
}

//These three functions filter the allCustomers array on the client side without any API call:
function filterCustomers(){
    currentCustomersPage=1;
    renderCustomerTable(getFilteredCustomers);
}

function getFilteredCustomers(){
    const searchText= document.getElementById('searchCustomers').value.toLowerCase();
    const selectedGender = document.getElementById('filterGender').value;
    const selectedStatus = document.getElementById('filterHealthStatus').value;
    
    return allCustomers.filter(function(customer){
        const matchesSearch = customer.CustomerFName.toLowerCase().includes(searchText)
        ||customer.CustomerSName.toLowerCase().includes(searchText)
        ||customer.CustomerPhoneNumber.toLowerCase().includes(searchText)

        const matchesGender = selectedGender === ''
            || customer.CustomerGender === selectedGender;

        const matchesStatus = selectedStatus === ''
            || customer.CustomerHealthStatus === selectedStatus;

        return matchesSearch && matchesGender && matchesStatus;
    });
    
}

//Open the Add modal
function openAddModal(){
    document.getElementById('modalCustomerTitle').textContent='Add New Customer';
    document.getElementById('fieldCustomerFName').value='';
    document.getElementById('fieldCustomerSName').value='';
    document.getElementById('fieldCustomerGender').value='';
    document.getElementById('fieldDateOfBirth').value='';
    document.getElementById('fieldCustomerPhoneNumber').value='';
    document.getElementById('fieldCustomerEmail').value='';
    document.getElementById('fieldCustomerAddress').value='';
    document.getElementById('fieldCustomerHealthStatus').value='';
    document.getElementById('btnSaveCustomer').setAttribute('data-mode', 'add');
    document.getElementById('modalAddCustomer').style.display = 'flex';
}

//Open the Edit Modal
async function openEditModal(customerID) {
    const response = await apiFetch(`http://127.0.0.1:5000/customer/${customerID}`);
    if (!response) return;
    const customer = await response.json();
    
    document.getElementById('modalCustomerTitle').textContent='Edit Customer';
    document.getElementById('fieldCustomerFName').value=customer.CustomerFName;
    document.getElementById('fieldCustomerSName').value=customer.CustomerSName;
    document.getElementById('fieldCustomerGender').value=customer.CustomerGender;
    document.getElementById('fieldDateOfBirth').value=customer.DateOfBirth;
    document.getElementById('fieldCustomerPhoneNumber').value=customer.CustomerPhoneNumber;
    document.getElementById('fieldCustomerEmail').value=customer.CustomerEmail;
    document.getElementById('fieldCustomerAddress').value=customer.CustomerAddress;
    document.getElementById('fieldCustomerHealthStatus').value=customer.CustomerHealthStatus;
    document.getElementById('btnSaveCustomer').setAttribute('data-id', customerID);
    document.getElementById('btnSaveCustomer').setAttribute('data-mode', 'edit');
    document.getElementById('modalAddCustomer').style.display = 'flex';
}

//Save supplier (add and edit)
async function saveCustomer() {
    const mode = document.getElementById('btnSaveCustomer').getAttribute('data-mode');
    const customerID =  document.getElementById('btnSaveCustomer').getAttribute('data-id');
    
    const payload = {
        CustomerFName: document.getElementById('fieldCustomerFName').value.trim(),
        CustomerSName: document.getElementById('fieldCustomerSName').value.trim(),
        CustomerGender: document.getElementById('fieldCustomerGender').value.trim(),
        DateOfBirth: document.getElementById('fieldDateOfBirth').value.trim(),
        CustomerPhoneNumber: document.getElementById('fieldCustomerPhoneNumber').value.trim(),
        CustomerEmail: document.getElementById('fieldCustomerEmail').value.trim(),
        CustomerAddress: document.getElementById('fieldCustomerAddress').value.trim(),
        CustomerHealthStatus: document.getElementById('fieldCustomerHealthStatus').value.trim(),  
    }

    if(!payload.CustomerFName || !payload.CustomerSName || !payload.CustomerGender || !payload.DateOfBirth || !payload.CustomerPhoneNumber || !payload.CustomerAddress || !payload.CustomerHealthStatus){
        alert('Please fill in all the fields');
        return;
    }

    const url = mode ==='add'
    ? 'http://127.0.0.1:5000/customer'
    : `http://127.0.0.1:5000/customer/${customerID}`;

    const method = mode ===  'add' ? 'POST' : 'PUT';

    const response = await apiFetch(url, {
        method: method,
        body: JSON.stringify(payload)
    });

    if(!response) return;

    if (response.ok) {
        document.getElementById('modalAddCustomer').style.display = 'none';
        loadCustomers();
    } else {
        const data = await response.json();
        alert(data.message || 'Something went wrong.');
    }
}

//Delete Customer
async function deleteCustomer(customerID) {
    if (!confirmDelete('Are you sure you want to delete this customer?')) return;

     const response = await apiFetch(`http://127.0.0.1:5000/customer/${customerID}`, {
        method: 'DELETE'
    });

    if (!response) return;

    if (response.ok) {
        loadCustomers();
    } else {
        const data = await response.json();
        alert(data.message || 'Could not delete Customer.');
    }
}
//Run everything on the page load
document.addEventListener('DOMContentLoaded', function() {
    loadCustomers();
});
    
