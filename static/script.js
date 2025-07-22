document.addEventListener('DOMContentLoaded', function() {
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