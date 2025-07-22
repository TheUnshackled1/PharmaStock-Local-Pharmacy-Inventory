document.addEventListener('DOMContentLoaded', function() {
    // Modal buy logic for home.html
    var modalBg = document.getElementById('buyModalBg');
    var modalProductName = document.getElementById('modalProductName');
    var confirmBuyBtn = document.getElementById('confirmBuyBtn');
    var cancelBuyBtn = document.getElementById('cancelBuyBtn');
    var selectedProduct = null;

    document.querySelectorAll('.product-card').forEach(function(card) {
        card.addEventListener('click', function() {
            selectedProduct = card;
            modalProductName.textContent = card.dataset.name;
            modalBg.style.display = 'flex';
        });
    });

    if (confirmBuyBtn) {
        confirmBuyBtn.onclick = function() {
            alert('Thank you for buying ' + (selectedProduct ? selectedProduct.dataset.name : '') + '!');
            modalBg.style.display = 'none';
        };
        confirmBuyBtn.focus();
    }
    if (cancelBuyBtn) {
        cancelBuyBtn.onclick = function() {
            modalBg.style.display = 'none';
        };
    }

    // Highlight row on hover for all tables
    document.querySelectorAll('table').forEach(function(table) {
        table.querySelectorAll('tr').forEach(function(row, idx) {
            if(idx === 0) return; // skip header
            row.addEventListener('mouseenter', function() {
                this.style.boxShadow = '0 2px 8px #1976d2';
                this.style.transform = 'scale(1.01)';
            });
            row.addEventListener('mouseleave', function() {
                this.style.boxShadow = '';
                this.style.transform = '';
            });
        });
    });
});