document.addEventListener('DOMContentLoaded', function() {
    console.log('script.js loaded and DOMContentLoaded fired.');
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

    // Barcode Modal Logic
    const barcodeModal = document.getElementById('barcodeModal');
    const barcodeImage = document.getElementById('barcodeImage');
    const closeModal = document.querySelector('.close-button');
    const viewBarcodeButtons = document.querySelectorAll('.view-barcode-btn');

    viewBarcodeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productPk;
            barcodeImage.src = `/barcode/${productId}/`; // Assuming your barcode URL is /barcode/<pk>/
            barcodeModal.style.display = 'block';
        });
    });

    closeModal.addEventListener('click', function() {
        barcodeModal.style.display = 'none';
        barcodeImage.src = ''; // Clear image source
    });

    window.addEventListener('click', function(event) {
        if (event.target == barcodeModal) {
            barcodeModal.style.display = 'none';
            barcodeImage.src = ''; // Clear image source
        }
    });
});