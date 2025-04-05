<script>
    // Tự động ẩn alert sau 3 giây
    setTimeout(function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.classList.remove('show');
    alert.classList.add('hide');
    });
  }, 3000);
</script>