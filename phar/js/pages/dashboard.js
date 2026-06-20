guardPage();

//This function checks if there are any expiring batches. 
// If there are, it shows the red banner. If there are none, it hides it.
async function loadExpiryBanner() {
    const response = await apiFetch('http://127.0.0.1:5000/alerts/expiry');
    if (!response) return;

    const data = await response.json();
    const banner = document.getElementById('expiryBanner');

    if (data.length > 0) {
        banner.style.display = 'flex';
        banner.querySelector('strong').textContent =
            data.length + ' batches expiring within 30 days.';
    } else {
        banner.style.display = 'none';
    }
}

//Same pattern as the expiry banner but for low stock:
async function loadLowStockBanner() {
    const response = await apiFetch('http://127.0.0.1:5000/alerts/low-stock');
    if (!response) return;

    const data = await response.json();
    const banner = document.getElementById('lowStockBanner');

    if (data.length > 0) {
        banner.style.display = 'flex';
        banner.querySelector('strong').textContent =
            data.length + ' products are low in stock.';
    } else {
        banner.style.display = 'none';
    }
}


//This function loads the numbers for all 6 stat cards on the dashboard.
//It makes three API calls and combines the results:
async function loadStatCards() {
    const [inventoryRes, salesRes, customersRes, reorderRes] = await Promise.all([
        apiFetch('http://127.0.0.1:5000/reports/inventory'),
        apiFetch('http://127.0.0.1:5000/reports/daily-sales'),
        apiFetch('http://127.0.0.1:5000/customer'),
        apiFetch('http://127.0.0.1:5000/reorder')
    ]);

    const inventory  = await inventoryRes.json();
    const sales      = await salesRes.json();
    const customers  = await customersRes.json();
    const reorders   = await reorderRes.json();

    document.getElementById('statTotalProducts').textContent =
        inventory.length;

    document.getElementById('statTodaySales').textContent =
        sales.length;

    document.getElementById('statLowStock').textContent =
        inventory.filter(p => p.StockStatus === 'Low Stock').length;

    document.getElementById('statExpiring').textContent =
        inventory.filter(p => p.StockStatus === 'Out of Stock').length;

    document.getElementById('statCustomers').textContent =
        customers.length;

    document.getElementById('statPendingReorders').textContent =
        reorders.filter(r => r.SuggestionStatus === 'Pending').length;
}

// Populate recent sales table
async function loadRecentSales() {
    const response = await apiFetch('http://127.0.0.1:5000/reports/daily-sales');
    if (!response) return;

    const sales = await response.json();
    const tbody = document.getElementById('recentSalesTable');
    tbody.innerHTML = '';

    if (sales.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center td-muted">No sales today yet.</td></tr>';
        return;
    }

    sales.slice(0, 5).forEach(function(sale) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="td-id">${formatID('S', sale.SaleID, 3)}</td>
            <td class="td-bold">${sale.BrandName}</td>
            <td class="td-muted">${sale.CustomerFName ? sale.CustomerFName + ' ' + sale.CustomerSName : 'Walk-in'}</td>
            <td>${formatCurrency(sale.TotalAmount)}</td>
            <td><span class="badge ${sale.PaymentMethod === 'Cash' ? 'badge-green' : 'badge-blue'}">${sale.PaymentMethod}</span></td>
        `;
        tbody.appendChild(row);
    });
}

// Populate expiry alerts table
async function loadExpiryTable() {
    const response = await apiFetch('http://127.0.0.1:5000/alerts/expiry');
    if (!response) return;

    const alerts = await response.json();
    const tbody = document.getElementById('expiryAlertsTable');
    tbody.innerHTML = '';

    if (alerts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center td-muted">No expiry alerts.</td></tr>';
        return;
    }

    alerts.forEach(function(item) {
        const badgeClass = item.DaysUntilExpiry <= 30 ? 'badge-red' : 'badge-amber';
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="td-bold">${item.BrandName}</td>
            <td class="td-id">${item.BatchNumber}</td>
            <td>${formatDate(item.ExpiryDate)}</td>
            <td>${item.QuantityRemaining}</td>
            <td><span class="badge ${badgeClass}">${item.DaysUntilExpiry} days</span></td>
        `;
        tbody.appendChild(row);
    });
}


// It runs all the functions above when the page loads:
document.addEventListener('DOMContentLoaded', function() {
    loadExpiryBanner();
    loadLowStockBanner();
    loadStatCards();
    loadRecentSales();
    loadExpiryTable();
});