// ============================================
// KASIRKU - Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function () {

    // Auto dismiss alert setelah 4 detik
    const alerts = document.querySelectorAll('.custom-alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });

    // Konfirmasi sebelum hapus
    window.confirmDelete = function (itemName) {
        return confirm('Yakin ingin menghapus ' + itemName + '? Aksi ini tidak bisa dibatalkan.');
    };

    // Aktifkan tooltip Bootstrap
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(function (el) {
        new bootstrap.Tooltip(el);
    });

    // Format angka input harga jadi lebih readable
    const priceInputs = document.querySelectorAll('input[name="price"]');
    priceInputs.forEach(function (input) {
        input.addEventListener('blur', function () {
            const val = parseFloat(this.value);
            if (!isNaN(val) && val < 0) {
                this.value = 0;
            }
        });
    });

    // Cegah submit form duplikat
    const forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        form.addEventListener('submit', function () {
            const submitBtn = form.querySelector('[type="submit"]');
            if (submitBtn && !form.dataset.submitting) {
                form.dataset.submitting = 'true';
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Memproses...';
            }
        });
    });

});