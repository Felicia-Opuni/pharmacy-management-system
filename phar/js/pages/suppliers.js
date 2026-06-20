guardPage()

//An array to hold all suppliers for
//to make the search and filtter functions work without making multiple API calls.
let allSuppliers = []

//This function fetches all suppliers from Flask and builds the table:
async function loadSuppliers() {
    const response = await apiFetch('http://localhost:5000/suppliers');
    if (!response) return;

    const data = await response.json();
    allSuppliers = data;
    renderSuppliersTable(allSuppliers);
    
}

//This function takes a list of suppliers and builds the table rows:
function renderSuppliersTable(suppliers) {
    const tbody = document.getElementById('suppliersTableBody');
    tbody.innerHTML = '';
    document.getElementById('supplierCount').textContent = 
    'Showing ' + suppliers.length + ' supplier' + (suppliers.length !== 1 ? 's' : '') + ' registered';

    if (suppliers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center td-muted">No suppliers found.</td></tr>';
        return;
    }

    suppliers.forEach(function(supplier) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="td-id">${formatID('SUP', supplier.SupplierID, 3)}</td>
            <td class="td-bold">${supplier.SupplierName}</td>
            <td>${supplier.SupplierPhoneNumber}</td>
            <td class="td-muted">${supplier.SupplierEmail}</td>
            <td>${supplier.SupplierAddress}</td>
            <td style="display:flex; gap:6px; flex-wrap:wrap;">
                <a href="/review/purchase_orders.html" class="btn btn-icon btn-sm" title="View Orders">📋</a></td>
            <td>
                <button class="btn btn-icon btn-sm" title="Edit" onclick="openEditModal(${supplier.SupplierID})">✏️</button>
                <button class="btn btn-icon btn-sm" title="Delete" onclick="deleteSupplier(${supplier.SupplierID})">🗑️</button>
            </td>
        `;
        tbody.appendChild(row);
    });   
}


//These three functions filter the allProducts array on the client side without any API call:
function filterSuppliers() {
    const searchText = document.getElementById('searchSuppliers').value.toLowerCase();
    
    const filtered = allSuppliers.filter(function(supplier){
        const matchesSearch = supplier.SupplierName.toLowerCase().includes(searchText)
        ||supplier.SupplierEmail.toLowerCase().includes(searchText)
        ||supplier.SupplierAddress.toLowerCase().includes(searchText);
        
        return matchesSearch;
    });

    renderSuppliersTable(filtered);
}


//Open the Add modal
function openAddModal(){
    document.getElementById('modalSupplierTitle').textContent = 'Add New Supplier';
    document.getElementById('fieldSupplierName').value='';
    document.getElementById('fieldSupplierPhone').value='';
    document.getElementById('fieldSupplierEmail').value='';
    document.getElementById('fieldSupplierAddress').value='';
    document.getElementById('btnSaveSupplier').setAttribute('data-mode', 'add');
    document.getElementById('modalSupplier').style.display = 'flex';
}

//Open the Edit Modal
async function openEditModal(supplierID) {
    const response = await apiFetch(`http://127.0.0.1:5000/suppliers/${supplierID}`);
    if (!response) return;

    const supplier = await response.json();
    document.getElementById('modalSupplierTitle').textContent = 'Edit Supplier';
    document.getElementById('fieldSupplierName').value=supplier.SupplierName;
    document.getElementById('fieldSupplierPhone').value=supplier.SupplierPhoneNumber;
    document.getElementById('fieldSupplierEmail').value=supplier.SupplierEmail;
    document.getElementById('fieldSupplierAddress').value=supplier.SupplierAddress;
    document.getElementById('btnSaveSupplier').setAttribute('data-id', supplierID);
    document.getElementById('btnSaveSupplier').setAttribute('data-mode', 'edit');
    document.getElementById('modalSupplier').style.display = 'flex';
}

//Save supplier (add and edit)
async function saveSupplier() {
    const mode = document.getElementById('btnSaveSupplier').getAttribute('data-mode');
    const supplierID =  document.getElementById('btnSaveSupplier').getAttribute('data-id');

    const payload = {
        SupplierName: document.getElementById('fieldSupplierName').value.trim(),
        SupplierPhoneNumber: document.getElementById('fieldSupplierPhone').value.trim(),
        SupplierEmail: document.getElementById('fieldSupplierEmail').value.trim(),
        SupplierAddress: document.getElementById('fieldSupplierAddress').value.trim(),
    }

    if (!payload.SupplierName || !payload.SupplierPhoneNumber || !payload.SupplierEmail || !payload.SupplierAddress){
        alert('Please fill in all the fields');
        return;
    }

    const url = mode === 'add'
    ? 'http://127.0.0.1:5000/suppliers'
    : `http://127.0.0.1:5000/suppliers/${supplierID}`;

    const method = mode === 'add' ? 'POST' : 'PUT';

    const response = await apiFetch(url, {
        method: method,
        body: JSON.stringify(payload)
    });
    
    if (!response) return;

    if (response.ok) {
        document.getElementById('modalSupplier').style.display = 'none';
        loadSuppliers();
    } else {
        const data = await response.json();
        alert(data.message || 'Something went wrong.');
    }
}

//Delete Supplier
async function deleteSupplier(supplierID) {
    if (!confirmDelete('Are you sure you want to delete this supplier?')) return;

    const response = await apiFetch(`http://127.0.0.1:5000/suppliers/${supplierID}`, {
        method: 'DELETE'
    });

    if (!response) return;

    if (response.ok) {
        loadSuppliers();
    } else {
        const data = await response.json();
        alert(data.message || 'Could not delete Supplier.');
    }
}
//Run everything on the page load
document.addEventListener('DOMContentLoaded', function() {
    loadSuppliers();
});