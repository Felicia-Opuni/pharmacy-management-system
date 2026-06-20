guardPage()

//An array to hold all products for
//to make the search and filtter functions work without making multiple API calls.
let allProducts = [];
let currentProductPage = 1;
const rowsPerPage = 10;

//This function fetches all products from Flask and builds the table:
async function loadProducts() {
    const response = await apiFetch('http://127.0.0.1:5000/products');
    if (!response) return;

    const data = await response.json();
    allProducts = data;
    renderProductsTable(allProducts);
}

//This function takes a list of products and builds the table rows:
function renderProductsTable(products) {
    const tbody = document.getElementById('productsTableBody');
    tbody.innerHTML = '';
    document.getElementById('productCount').textContent = 
    'Showing ' + products.length + ' of ' + allProducts.length + ' products';

    if (products.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center td-muted">No products found.</td></tr>';
        return;
    }

    const start = (currentProductPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const pageRows = products.slice(start, end);

    pageRows.forEach(function(product) {
        const statusBadge = product.StockStatus === 'In Stock'
            ? '<span class="badge badge-green">In Stock</span>'
            : product.StockStatus === 'Low Stock'
            ? '<span class="badge badge-amber">Low Stock</span>'
            : '<span class="badge badge-red">Out of Stock</span>';

        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="td-id">${formatID('P', product.ProductID, 3)}</td>
            <td><span class="badge badge-blue">${product.CategoryName}</span></td>
            <td class="td-bold">${product.GenericName}</td>
            <td>${product.BrandName}</td>
            <td>${formatCurrency(product.SellingPrice)}</td>
            <td>${product.ReorderLevel}</td>
            <td>${product.TotalStock ?? 0}</td>
            <td>${statusBadge}</td>
            <td>
                <button class="btn btn-icon btn-sm" onclick="openEditModal(${product.ProductID})">✏️</button>
                <button class="btn btn-icon btn-sm" onclick="deleteProduct(${product.ProductID})">🗑️</button>
            </td>
        `;
        tbody.appendChild(row);
    });
    renderProductsPagination(products);
}

function renderProductsPagination(products) {
    const pagination = document.getElementById('productsPagination');
    pagination.innerHTML = '';

    const totalPages = Math.ceil(products.length / rowsPerPage);

    if (totalPages <= 1) {
        pagination.style.display = 'none';
        return;
    }

    pagination.style.display = 'flex';

    const prevBtn = document.createElement('button');
    prevBtn.className = 'page-btn' + (currentProductPage === 1 ? ' disabled' : '');
    prevBtn.textContent = '‹';
    prevBtn.onclick = function() {
        if (currentProductPage > 1) {
            currentProductPage--;
            renderProductsTable(getFilteredProducts());
        }
    };
    pagination.appendChild(prevBtn);

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.className = 'page-btn' + (i === currentProductPage ? ' active' : '');
        btn.textContent = i;
        btn.onclick = function() {
            currentProductPage = i;
            renderProductsTable(getFilteredProducts());
        };
        pagination.appendChild(btn);
    }

    const nextBtn = document.createElement('button');
    nextBtn.className = 'page-btn' + (currentProductPage === totalPages ? ' disabled' : '');
    nextBtn.textContent = '›';
    nextBtn.onclick = function() {
        if (currentProductPage < totalPages) {
            currentProductPage++;
            renderProductsTable(getFilteredProducts());
        }
    };
    pagination.appendChild(nextBtn);
}

//These three functions filter the allProducts array on the client side without any API call:
function filterProducts() {
    currentProductPage=1;
    renderProductsTable(getFilteredProducts());
}

function getFilteredProducts() {
    const searchText = document.getElementById('searchProducts').value.toLowerCase();
    const selectedCategory = document.getElementById('filterCategory').value;
    const selectedStatus = document.getElementById('filterStatus').value;

    return allProducts.filter(function(product) {
        const matchesSearch = product.GenericName.toLowerCase().includes(searchText)
            || product.BrandName.toLowerCase().includes(searchText);
        const matchesCategory = selectedCategory === '' || product.CategoryName === selectedCategory;
        const matchesStatus = selectedStatus === '' || product.StockStatus === selectedStatus;
        return matchesSearch && matchesCategory && matchesStatus;
    });
}

//Open the Add modal
function openAddModal() {
    document.getElementById('modalProductTitle').textContent = 'Add New Product';
    document.getElementById('fieldGenericName').value = '';
    document.getElementById('fieldBrandName').value = '';
    document.getElementById('fieldCategory').value = '';
    document.getElementById('fieldSellingPrice').value = '';
    document.getElementById('fieldReorderLevel').value = '';
    document.getElementById('btnSaveProduct').setAttribute('data-mode', 'add');
    document.getElementById('btnSaveProduct').removeAttribute('data-id');
    document.getElementById('modalProduct').style.display = 'flex';
}


// Open the Edit modal
async function openEditModal(productID) {
    const response = await apiFetch(`http://127.0.0.1:5000/products/${productID}`);
    if (!response) return;

    const product = await response.json();

    document.getElementById('modalProductTitle').textContent = 'Edit Product';
    document.getElementById('fieldGenericName').value = product.GenericName;
    document.getElementById('fieldBrandName').value = product.BrandName;
    document.getElementById('fieldCategory').value = product.CategoryName;
    document.getElementById('fieldSellingPrice').value = product.SellingPrice;
    document.getElementById('fieldReorderLevel').value = product.ReorderLevel;
    document.getElementById('btnSaveProduct').setAttribute('data-mode', 'edit');
    document.getElementById('btnSaveProduct').setAttribute('data-id', productID);
    document.getElementById('modalProduct').style.display = 'flex';
}


// Save product (Add and Edit)
async function saveProduct() {
    const mode = document.getElementById('btnSaveProduct').getAttribute('data-mode');
    const productID = document.getElementById('btnSaveProduct').getAttribute('data-id');

    const payload = {
        GenericName:   document.getElementById('fieldGenericName').value.trim(),
        BrandName:     document.getElementById('fieldBrandName').value.trim(),
        CategoryName:  document.getElementById('fieldCategory').value,
        SellingPrice:  document.getElementById('fieldSellingPrice').value,
        ReorderLevel:  document.getElementById('fieldReorderLevel').value
    };

    if (!payload.GenericName || !payload.BrandName || !payload.CategoryName
        || !payload.SellingPrice || !payload.ReorderLevel) {
        alert('Please fill in all fields.');
        return;
    }

    const url = mode === 'add'
        ? 'http://127.0.0.1:5000/products'
        : `http://127.0.0.1:5000/products/${productID}`;

    const method = mode === 'add' ? 'POST' : 'PUT';

    const response = await apiFetch(url, {
        method: method,
        body: JSON.stringify(payload)
    });

    if (!response) return;

    if (response.ok) {
        document.getElementById('modalProduct').style.display = 'none';
        loadProducts();
    } else {
        const data = await response.json();
        alert(data.message || 'Something went wrong.');
    }
}


//Delete product
async function deleteProduct(productID) {
    if (!confirmDelete('Are you sure you want to delete this product?')) return;

    const response = await apiFetch(`http://127.0.0.1:5000/products/${productID}`, {
        method: 'DELETE'
    });

    if (!response) return;

    if (response.ok) {
        loadProducts();
    } else {
        const data = await response.json();
        alert(data.message || 'Could not delete product.');
    }
}

//Run everything on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
});

