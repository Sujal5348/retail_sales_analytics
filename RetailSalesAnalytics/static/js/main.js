/* ============================================================
   Retail Sales Analytics System - Interactive Javascript
   ============================================================ */

document.addEventListener("DOMContentLoaded", function() {
    if (document.getElementById("monthlySalesChart")) {
        loadDashboardCharts();
    }
});

function loadDashboardCharts() {
    fetch('/api/dashboard-charts')
        .then(response => response.json())
        .then(data => {
            renderMonthlySalesChart(data.monthly_trend);
            renderCategoryChart(data.category_perf);
            renderRegionalChart(data.regional_sales);
            renderPaymentMethodChart(data.payment_methods);
        })
        .catch(err => console.error("Error loading dashboard charts:", err));
}

function renderMonthlySalesChart(trends) {
    const dates = trends.map(t => t.YearMonth);
    const revenues = trends.map(t => t.Revenue);
    const profits = trends.map(t => t.Profit);

    const trace1 = {
        x: dates,
        y: revenues,
        name: 'Revenue ($)',
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#38BDF8', width: 3 },
        marker: { size: 6 }
    };

    const trace2 = {
        x: dates,
        y: profits,
        name: 'Gross Profit ($)',
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#10B981', width: 3, dash: 'dot' },
        marker: { size: 6 }
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#94A3B8' },
        margin: { t: 20, r: 20, l: 50, b: 50 },
        xaxis: { gridcolor: '#334155' },
        yaxis: { gridcolor: '#334155', tickprefix: '$' },
        legend: { orientation: 'h', y: 1.15 }
    };

    Plotly.newPlot('monthlySalesChart', [trace1, trace2], layout, { responsive: true });
}

function renderCategoryChart(categories) {
    const names = categories.map(c => c.CategoryName);
    const revenues = categories.map(c => c.TotalRevenue);

    const trace = {
        x: revenues,
        y: names,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#6366F1' }
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#94A3B8' },
        margin: { t: 20, r: 20, l: 150, b: 40 },
        xaxis: { gridcolor: '#334155', tickprefix: '$' },
        yaxis: { gridcolor: '#334155', autorange: 'reversed' }
    };

    Plotly.newPlot('categorySalesChart', [trace], layout, { responsive: true });
}

function renderRegionalChart(regions) {
    const labels = regions.map(r => r.Region);
    const values = regions.map(r => r.Revenue);

    const trace = {
        labels: labels,
        values: values,
        type: 'pie',
        hole: 0.5,
        marker: { colors: ['#38BDF8', '#6366F1', '#10B981', '#F59E0B', '#F43F5E'] }
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#94A3B8' },
        margin: { t: 20, r: 20, l: 20, b: 20 },
        legend: { orientation: 'h' }
    };

    Plotly.newPlot('regionalSalesChart', [trace], layout, { responsive: true });
}

function renderPaymentMethodChart(methods) {
    const labels = methods.map(m => m.PaymentMethod);
    const values = methods.map(m => m.TotalVolume);

    const trace = {
        x: labels,
        y: values,
        type: 'bar',
        marker: { color: '#F59E0B' }
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#94A3B8' },
        margin: { t: 20, r: 20, l: 50, b: 50 },
        xaxis: { gridcolor: '#334155' },
        yaxis: { gridcolor: '#334155', tickprefix: '$' }
    };

    Plotly.newPlot('paymentMethodChart', [trace], layout, { responsive: true });
}

// Order detail modal viewer
function viewOrderDetail(orderId) {
    fetch(`/sales/api/order/${orderId}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("modalOrderId").innerText = `#ORD-${data.OrderID}`;
            document.getElementById("modalCustomer").innerText = data.CustomerName;
            document.getElementById("modalStore").innerText = data.StoreName;
            document.getElementById("modalEmployee").innerText = data.EmployeeName;
            document.getElementById("modalDate").innerText = data.OrderDate;
            document.getElementById("modalPayment").innerText = data.PaymentMethod;
            document.getElementById("modalTotal").innerText = `$${data.TotalAmount.toFixed(2)}`;

            let rows = "";
            data.items.forEach(item => {
                rows += `
                    <tr>
                        <td>${item.SKU}</td>
                        <td>${item.ProductName}</td>
                        <td>${item.Quantity}</td>
                        <td>$${item.UnitPrice.toFixed(2)}</td>
                        <td>${item.Discount}%</td>
                        <td class="fw-bold">$${item.LineTotal.toFixed(2)}</td>
                    </tr>
                `;
            });
            document.getElementById("modalOrderItems").innerHTML = rows;

            const modal = new bootstrap.Modal(document.getElementById('orderDetailModal'));
            modal.show();
        });
}
